from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from audit.models import AuditLog
from audit.middleware import get_current_user
from .models import Resident


@receiver(pre_save, sender=Resident)
def detect_resident_archive_status(sender, instance, **kwargs):
    """
    Detect archive/unarchive events by tracking is_active field changes.
    Store the old value so post_save can compare.
    """
    if instance.pk:
        try:
            old_instance = Resident.objects.get(pk=instance.pk)
            instance._old_is_active = old_instance.is_active
        except Resident.DoesNotExist:
            instance._old_is_active = None
    else:
        instance._old_is_active = None


@receiver(post_save, sender=Resident)
def log_resident_activity(sender, instance, created, **kwargs):
    """
    Automatically log resident creation, updates, archive and unarchive to the audit log.
    """
    user = get_current_user() or instance.created_by
    
    if created:
        # Log creation
        AuditLog.objects.create(
            user=user,
            action='CREATE_RESIDENT',
            target_model='Resident',
            target_id=instance.pk,
            description=f"Created resident: {instance.first_name} {instance.last_name} (Room {instance.room_number})"
        )
    else:
        # Check for archive/unarchive first
        if hasattr(instance, '_old_is_active') and instance._old_is_active is not None:
            if instance._old_is_active != instance.is_active:
                # Log archive/unarchive
                if instance.is_active is False:
                    AuditLog.objects.create(
                        user=user,
                        action='ARCHIVE_RESIDENT',
                        target_model='Resident',
                        target_id=instance.pk,
                        description=f"Archived resident: {instance.first_name} {instance.last_name}"
                    )
                else:
                    AuditLog.objects.create(
                        user=user,
                        action='UNARCHIVE_RESIDENT',
                        target_model='Resident',
                        target_id=instance.pk,
                        description=f"Unarchived resident: {instance.first_name} {instance.last_name}"
                    )
                return  # Don't log as update
        
        # Log regular update
        AuditLog.objects.create(
            user=user,
            action='UPDATE_RESIDENT',
            target_model='Resident',
            target_id=instance.pk,
            description=f"Updated resident: {instance.first_name} {instance.last_name}"
        )
