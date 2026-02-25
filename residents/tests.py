from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from .models import Resident

User = get_user_model()

class ResidentTestCase(TestCase):
    def setUp(self):
        # Create users
        self.manager = User.objects.create_user(
            username='manager', password='pass1234', role='MANAGER', is_approved=True
        )
        self.carer = User.objects.create_user(
            username='carer', password='pass1234', role='CARER', is_approved=True
        )

        # Create a resident
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
            # Minimal careplan data to satisfy validation
            'review_date': date.today()
        })
        self.assertEqual(response.status_code, 302)  # redirect on success
        self.assertTrue(Resident.objects.filter(first_name='Alice').exists())

    def test_resident_create_view_carer_redirect(self):
        self.client.login(username='carer', password='pass1234')
        response = self.client.get(reverse('residents:create'))
        self.assertEqual(response.status_code, 302)  # carer redirected away

    def test_archive_unarchive_resident(self):
        self.client.login(username='manager', password='pass1234')
        # Archive resident
        response = self.client.post(reverse('residents:archive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertFalse(self.resident.is_active)

        # Unarchive resident
        response = self.client.post(reverse('residents:unarchive', args=[self.resident.pk]))
        self.resident.refresh_from_db()
        self.assertTrue(self.resident.is_active)
        

        