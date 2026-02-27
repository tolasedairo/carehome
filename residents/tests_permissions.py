from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from residents.models import Resident

User = get_user_model()


class ResidentPermissionsAndArchiveTestCase(TestCase):
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
            first_name='John', last_name='Doe', date_of_birth='1950-01-01',
            gender='MALE', room_number='101',
            emergency_contact_name='Jane Doe', emergency_contact_phone='123456789',
            created_by=self.manager
        )

    def test_archive_unarchive_resident_manager(self):
        # Manager can archive
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('residents:archive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertFalse(self.resident.is_active)
        self.assertEqual(response.status_code, 302)

        # Manager can unarchive
        response = self.client.post(reverse('residents:unarchive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertTrue(self.resident.is_active)
        self.assertEqual(response.status_code, 302)

    def test_archive_unarchive_resident_carer_redirect(self):
        # Carer cannot archive
        self.client.login(username='carer', password='pass1234')
        response = self.client.post(reverse('residents:archive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertTrue(self.resident.is_active)
        self.assertEqual(response.status_code, 302)  # redirected

        # Carer cannot unarchive
        self.resident.is_active = False
        self.resident.save()
        response = self.client.post(reverse('residents:unarchive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertFalse(self.resident.is_active)
        self.assertEqual(response.status_code, 302)  # redirected

    def test_archived_resident_list_manager_only(self):
        # Archive the resident first
        self.resident.is_active = False
        self.resident.save()

        # Manager can access archived list
        self.client.login(username='manager', password='pass1234')
        response = self.client.get(reverse('residents:archived'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

        # Carer cannot access archived list
        self.client.login(username='carer', password='pass1234')
        response = self.client.get(reverse('residents:archived'))
        self.assertEqual(response.status_code, 302)  # redirected
