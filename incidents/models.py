from django.db import models
from django.conf import settings
from residents.models import Resident


class Incident(models.Model):
    INCIDENT_TYPE_CHOICES = (
        ('FALL', 'Fall'),
        ('MED_ERROR', 'Medication Error'),
        ('BEHAVIOR', 'Behavioural Incident'),
        ('OTHER', 'Other'),
    )

    resident = models.ForeignKey(
        Resident,
        on_delete=models.CASCADE,
        related_name='incidents',
        blank=True,
        null=True
    )
    incident_type = models.CharField(
        max_length=20,
        choices=INCIDENT_TYPE_CHOICES
    )
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='incidents_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        resident_name = self.resident or 'General'
        return f"{self.get_incident_type_display()} - {resident_name}"

    class Meta:
        ordering = ['-created_at']
