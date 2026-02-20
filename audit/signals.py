from django.db.models.signals import post_save
from django.dispatch import receiver
from residents.models import Resident
from careplans.models import CarePlan
from handovers.models import Handover
from incidents.models import Incident
from audit.models import AuditLog

# Example: Log Resident creation
@receiver(post_save, sender=Resident)
def log_resident(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            user=instance.created_by,
            action='CREATE_RESIDENT',
            target_model='Resident',
            target_id=instance.id,
            description=f"Resident {instance} created."
        )