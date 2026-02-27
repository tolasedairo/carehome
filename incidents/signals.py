from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from audit.models import AuditLog
from audit.middleware import get_current_user
from .models import Incident


def _is_manager(user):
    return bool(user and getattr(user, "role", None) == "MANAGER")


@receiver(pre_save, sender=Incident)
def detect_incident_resolution(sender, instance, **kwargs):
    """
    Detect resolution status change by tracking is_resolved field.
    """
    if instance.pk:
        try:
            old_instance = Incident.objects.get(pk=instance.pk)
            instance._old_is_resolved = old_instance.is_resolved
        except Incident.DoesNotExist:
            instance._old_is_resolved = None
    else:
        instance._old_is_resolved = None


@receiver(post_save, sender=Incident)
def log_incident_activity(sender, instance, created, **kwargs):
    """
    Automatically log incident creation, updates, and resolution to the audit log.
    """
    user = get_current_user() or instance.created_by
    if not _is_manager(user):
        return
    resident_str = f" for {instance.resident}" if instance.resident else " (General)"

    if created:
        # Log creation
        AuditLog.objects.create(
            user=user,
            action='CREATE_INCIDENT',
            target_model='Incident',
            target_id=instance.pk,
            description=f"Created incident: {instance.get_incident_type_display()}{resident_str}"
        )
    else:
        # Check for resolution first
        if hasattr(instance, '_old_is_resolved') and instance._old_is_resolved is not None:
            if instance._old_is_resolved != instance.is_resolved and instance.is_resolved is True:
                # Log resolution
                AuditLog.objects.create(
                    user=user,
                    action='RESOLVE_INCIDENT',
                    target_model='Incident',
                    target_id=instance.pk,
                    description=f"Resolved incident: {instance.get_incident_type_display()}{resident_str}"
                )
                return  # Don't log as update

        # Log regular update
        AuditLog.objects.create(
            user=user,
            action='UPDATE_INCIDENT',
            target_model='Incident',
            target_id=instance.pk,
            description=f"Updated incident: {instance.get_incident_type_display()}{resident_str}"
        )
