from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from audit.models import AuditLog
from audit.middleware import get_current_user
from .models import CarePlan


def _is_manager(user):
    return bool(user and getattr(user, "role", None) == "MANAGER")


@receiver(pre_save, sender=CarePlan)
def detect_careplan_archive_status(sender, instance, **kwargs):
    """
    Detect archive/unarchive events by tracking is_active field changes.
    """
    if instance.pk:
        try:
            old_instance = CarePlan.objects.get(pk=instance.pk)
            instance._old_is_active = old_instance.is_active
        except CarePlan.DoesNotExist:
            instance._old_is_active = None
    else:
        instance._old_is_active = None


@receiver(post_save, sender=CarePlan)
def log_careplan_activity(sender, instance, created, **kwargs):
    """
    Automatically log care plan creation, updates, archive and unarchive to the audit log.
    """
    user = get_current_user() or instance.created_by
    if not _is_manager(user):
        return

    if created:
        # Log creation
        AuditLog.objects.create(
            user=user,
            action='CREATE_CAREPLAN',
            target_model='CarePlan',
            target_id=instance.pk,
            description=f"Created care plan '{instance.title}' for {instance.resident}"
        )
    else:
        # Check for archive/unarchive first
        if hasattr(instance, '_old_is_active') and instance._old_is_active is not None:
            if instance._old_is_active != instance.is_active:
                # Log archive/unarchive
                if instance.is_active is False:
                    AuditLog.objects.create(
                        user=user,
                        action='ARCHIVE_CAREPLAN',
                        target_model='CarePlan',
                        target_id=instance.pk,
                        description=f"Archived care plan '{instance.title}' for {instance.resident}"
                    )
                else:
                    AuditLog.objects.create(
                        user=user,
                        action='UNARCHIVE_CAREPLAN',
                        target_model='CarePlan',
                        target_id=instance.pk,
                        description=f"Unarchived care plan '{instance.title}' for {instance.resident}"
                    )
                return  # Don't log as update

        # Log regular update
        AuditLog.objects.create(
            user=user,
            action='UPDATE_CAREPLAN',
            target_model='CarePlan',
            target_id=instance.pk,
            description=f"Updated care plan '{instance.title}' for {instance.resident}"
        )
