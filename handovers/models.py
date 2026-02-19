from django.db import models
from django.conf import settings
from residents.models import Resident


class Handover(models.Model):

    SHIFT_CHOICES = (
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('NIGHT', 'Night'),
    )

    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('NORMAL', 'Normal'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )

    title = models.CharField(max_length=200)
    resident = models.ForeignKey(
        Resident,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handovers'
    )

    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='NORMAL'
    )
    notes = models.TextField()
    is_completed = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='handovers_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.shift}"

    class Meta:
        ordering = ['-created_at']