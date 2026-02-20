from django.db import models
from django.conf import settings
from residents.models import Resident

# Create your models here.
class CarePlan(models.Model):

    resident = models.ForeignKey(
        Resident,
        on_delete=models.CASCADE,
        related_name='care_plans'
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    review_date = models.DateField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='careplans_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.resident} - {self.title}"

    class Meta:
        ordering = ['-created_at']