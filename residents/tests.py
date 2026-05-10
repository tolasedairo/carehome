# residents/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from .models import Resident

User = get_user_model()


class ResidentTestCase(TestCase):
    """Tests for resident creation, list view, and careplan integration"""

    def setUp(self):
        # Users
        self.manager = User.objects.create_user(
            username='manager', password='pass1234', role='MANAGER', is_approved=True
        )
        self.carer = User.objects.create_user(
            username='carer', password='pass1234', role='CARER', is_approved=True
        )

        # Resident
        self.resident = Resident.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1950-01-01',
            gender='MALE',
            room_number='101',
            emergency_contact_name='Jane Doe',
            emergency_contact_phone='123456789',
            created_by=self.manager
        )

    def test_resident_list_view(self):
        self.client.login(username='manager', password='pass1234')
        response = self.client.get(reverse('residents:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_resident_create_view_manager_only(self):
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('residents:create'), {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'date_of_birth': '1980-05-05',
            'gender': 'FEMALE',
            'room_number': '102',
            'emergency_contact_name': 'Bob Smith',
            'emergency_contact_phone': '987654321',
            # Minimal careplan data
            'review_date': date.today()
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Resident.objects.filter(first_name='Alice').exists())

    def test_resident_create_view_carer_redirect(self):
        self.client.login(username='carer', password='pass1234')
        response = self.client.get(reverse('residents:create'))
        self.assertEqual(response.status_code, 302)  # Carer should be redirected


class ResidentPermissionsAndArchiveTestCase(TestCase):
    """Tests for manager-only archive/unarchive permissions"""

    def setUp(self):
        self.manager = User.objects.create_user(
            username='manager', password='pass1234', role='MANAGER', is_approved=True
        )
        self.carer = User.objects.create_user(
            username='carer', password='pass1234', role='CARER', is_approved=True
        )
        self.resident = Resident.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1950-01-01',
            gender='MALE',
            room_number='101',
            emergency_contact_name='Jane Doe',
            emergency_contact_phone='123456789',
            created_by=self.manager
        )

    def test_archive_unarchive_resident_manager(self):
        self.client.login(username='manager', password='pass1234')

        # Archive
        self.client.post(reverse('residents:archive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertFalse(self.resident.is_active)

        # Unarchive
        self.client.post(reverse('residents:unarchive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertTrue(self.resident.is_active)

    def test_archive_unarchive_resident_carer_redirect(self):
        self.client.login(username='carer', password='pass1234')

        # Archive attempt
        self.client.post(reverse('residents:archive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertTrue(self.resident.is_active)  # Should remain active

        # Unarchive attempt
        self.client.post(reverse('residents:unarchive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertTrue(self.resident.is_active)  # Should remain active


class ResidentDeletePermissionTests(TestCase):
    """Tests for manager-only access to delete selection and delete endpoint."""

    def setUp(self):
        self.manager = User.objects.create_user(
            username='manager', password='pass1234', role='MANAGER', is_approved=True
        )
        self.carer = User.objects.create_user(
            username='carer', password='pass1234', role='CARER', is_approved=True
        )

        # Active resident
        self.active = Resident.objects.create(
            first_name='John', last_name='Doe', date_of_birth='1950-01-01',
            gender='MALE', room_number='101', emergency_contact_name='Jane',
            emergency_contact_phone='123', created_by=self.manager
        )

        # Archived resident (candidate for permanent deletion)
        self.archived = Resident.objects.create(
            first_name='Archived', last_name='User', date_of_birth='1940-01-01',
            gender='FEMALE', room_number='102', emergency_contact_name='Ann',
            emergency_contact_phone='321', created_by=self.manager, is_active=False
        )

    def test_manager_can_view_delete_select(self):
        self.client.login(username='manager', password='pass1234')
        response = self.client.get(reverse('residents:delete_select'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Archived User')

    def test_non_manager_cannot_view_delete_select(self):
        self.client.login(username='carer', password='pass1234')
        response = self.client.get(reverse('residents:delete_select'))
        self.assertEqual(response.status_code, 302)

    def test_delete_endpoint_get_blocked_and_no_delete(self):
        self.client.login(username='manager', password='pass1234')
        response = self.client.get(reverse('residents:delete', args=[self.archived.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Resident.objects.filter(pk=self.archived.pk).exists())

    def test_manager_can_delete_archived_resident(self):
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('residents:delete', args=[self.archived.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Resident.objects.filter(pk=self.archived.pk).exists())

    def test_manager_cannot_delete_active_resident(self):
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('residents:delete', args=[self.active.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Resident.objects.filter(pk=self.active.pk).exists())
