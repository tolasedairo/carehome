from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from residents.models import Resident
from incidents.models import Incident
from audit.models import AuditLog

# Create your tests here.
User = get_user_model()


class IncidentTestCase(TestCase):

    def setUp(self):
        self.manager = User.objects.create_user(
            username='manager',
            password='pass1234',
            role='MANAGER',
            is_approved=True
        )

        self.carer = User.objects.create_user(
            username='carer',
            password='pass1234',
            role='CARER',
            is_approved=True
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

    def test_incident_create(self):
        self.client.login(username='carer', password='pass1234')

        response = self.client.post(reverse('incidents:create'), {
            'resident': self.resident.id,
            'incident_type': 'FALL',
            'description': 'Slipped in bathroom'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Incident.objects.filter(description='Slipped in bathroom').exists())

        # ✅ Audit log created
        self.assertTrue(
            AuditLog.objects.filter(
                action='CREATE_INCIDENT',
                target_model='Incident'
            ).exists()
        )

    def test_incident_resolve(self):
        self.client.login(username='manager', password='pass1234')

        incident = Incident.objects.create(
            resident=self.resident,
            incident_type='FALL',
            description='Test incident',
            created_by=self.manager
        )

        response = self.client.post(reverse('incidents:resolve', args=[incident.pk]))

        self.assertEqual(response.status_code, 302)

        incident.refresh_from_db()
        self.assertTrue(incident.is_resolved)

        # ✅ Audit log created
        self.assertTrue(
            AuditLog.objects.filter(
                action='RESOLVE_INCIDENT',
                target_id=incident.id
            ).exists()
        )

    def test_unapproved_user_blocked(self):
        unapproved = User.objects.create_user(
            username='pending',
            password='pass1234',
            role='CARER',
            is_approved=False
        )

        self.client.login(username='pending', password='pass1234')

        response = self.client.get(reverse('incidents:create'))

        # Should redirect because approval_required decorator blocks
        self.assertEqual(response.status_code, 302)