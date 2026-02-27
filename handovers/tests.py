from django.test import TestCase
from django.contrib.auth import get_user_model
from residents.models import Resident
from handovers.models import Handover


# Create your tests here.
User = get_user_model()


class HandoverTestCase(TestCase):
    def setUp(self):
        self.carer = User.objects.create_user(
            username='carer', password='pass1234', role='CARER', is_approved=True
        )
        self.resident = Resident.objects.create(
            first_name='John', last_name='Doe', date_of_birth='1950-01-01',
            gender='MALE', room_number='101',
            emergency_contact_name='Jane Doe', emergency_contact_phone='123456789',
            created_by=self.carer
        )
        self.handover = Handover.objects.create(
            title='Morning Handover',
            resident=self.resident,
            shift='MORNING',
            priority='HIGH',
            notes='Patient stable',
            created_by=self.carer
        )

    def test_handover_str(self):
        self.assertIn('Morning Handover', str(self.handover))
        self.assertIn('Morning', str(self.handover))
        self.assertEqual(self.handover.resident, self.resident)
