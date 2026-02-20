from django.db import models
from django.conf import settings

# Create your models here.
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE_RESIDENT', 'Created Resident'),
        ('UPDATE_RESIDENT', 'Updated Resident'),
        ('ARCHIVE_RESIDENT', 'Archived Resident'),
        ('DELETE_RESIDENT', 'Deleted Resident'),
        ('CREATE_CAREPLAN', 'Created Care Plan'),
        ('UPDATE_CAREPLAN', 'Updated Care Plan'),
        ('CREATE_HANDOVER', 'Created Handover'),
        ('UPDATE_HANDOVER', 'Updated Handover'),
        ('CREATE_INCIDENT', 'Created Incident'),
        ('USER_APPROVAL', 'User Approved'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_model = models.CharField(max_length=50, blank=True, null=True)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"