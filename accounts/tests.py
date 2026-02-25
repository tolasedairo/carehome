from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
User = get_user_model()

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.carer = User.objects.create_user(
            username='carer', password='pass1234', role='CARER', is_approved=False
        )

    def test_user_str(self):
        self.assertEqual(str(self.carer), 'carer (CARER)')

    def test_user_approval_flag(self):
        self.assertFalse(self.carer.is_approved)
        self.carer.is_approved = True
        self.carer.save()
        self.assertTrue(User.objects.get(username='carer').is_approved)