from django.test import TestCase
from django.contrib.auth import get_user_model
from audit.models import AuditLog

# Create your tests here.
User = get_user_model()

class AuditLogTestCase(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username='manager', password='pass1234', role='MANAGER', is_approved=True
        )
        self.audit = AuditLog.objects.create(
            user=self.manager,
            action='CREATE_RESIDENT',
            target_model='Resident',
            target_id=1,
            description='Created resident John Doe'
        )

    def test_audit_str(self):
        self.assertIn('CREATE_RESIDENT', str(self.audit))
        self.assertIn('manager', str(self.audit))