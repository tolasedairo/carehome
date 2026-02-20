from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from audit.models import AuditLog
from audit.middleware import get_current_user
from .models import Handover


@receiver(pre_save, sender=Handover)
def detect_handover_completion(sender, instance, **kwargs):
    """
    Detect completion status change by tracking is_completed field.
    """
    if instance.pk:
        try:
            old_instance = Handover.objects.get(pk=instance.pk)
            instance._old_is_completed = old_instance.is_completed
        except Handover.DoesNotExist:
            instance._old_is_completed = None
    else:
        instance._old_is_completed = None


@receiver(post_save, sender=Handover)
def log_handover_activity(sender, instance, created, **kwargs):
    """
    Automatically log handover creation, updates, and completion to the audit log.
    """
    user = get_current_user() or instance.created_by
    resident_str = f" for {instance.resident}" if instance.resident else ""
    
    if created:
        # Log creation
        AuditLog.objects.create(
            user=user,
            action='CREATE_HANDOVER',
            target_model='Handover',
            target_id=instance.pk,
            description=f"Created handover '{instance.title}' ({instance.get_shift_display()} shift){resident_str}"
        )
    else:
        # Check for completion first
        if hasattr(instance, '_old_is_completed') and instance._old_is_completed is not None:
            if instance._old_is_completed != instance.is_completed and instance.is_completed is True:
                # Log completion
                AuditLog.objects.create(
                    user=user,
                    action='COMPLETE_HANDOVER',
                    target_model='Handover',
                    target_id=instance.pk,
                    description=f"Completed handover '{instance.title}'{resident_str}"
                )
                return  # Don't log as update
        
        # Log regular update
        AuditLog.objects.create(
            user=user,
            action='UPDATE_HANDOVER',
            target_model='Handover',
            target_id=instance.pk,
            description=f"Updated handover '{instance.title}'{resident_str}"
        )
