from django.test import TestCase
from django.contrib.auth import get_user_model
from residents.models import Resident
from incidents.models import Incident

User = get_user_model()

class IncidentTestCase(TestCase):
    def setUp(self):
        # Create a manager and a resident
        self.manager = User.objects.create_user(
            username='manager', password='pass1234', role='MANAGER', is_approved=True
        )
        self.resident = Resident.objects.create(
            first_name='John', last_name='Doe', date_of_birth='1950-01-01',
            gender='MALE', room_number='101',
            emergency_contact_name='Jane Doe', emergency_contact_phone='123456789',
            created_by=self.manager
        )
        self.incident = Incident.objects.create(
            resident=self.resident,
            incident_type='FALL',
            description='Slipped in bathroom',
            created_by=self.manager
        )

    def test_incident_str(self):
        self.assertIn('Fall', str(self.incident))
        self.assertIn('John', str(self.incident))

    def test_incident_resident_link(self):
        self.assertEqual(self.incident.resident, self.resident)