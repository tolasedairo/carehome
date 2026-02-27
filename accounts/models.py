from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds role and approval system.
    """

    ROLE_CHOICES = (
        ('MANAGER', 'Manager'),
        ('SENIOR', 'Senior Carer/Nurse'),
        ('CARER', 'Carer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CARER'
    )

    is_approved = models.BooleanField(
        default=False,
        help_text="Designates whether the manager has approved this account."
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
