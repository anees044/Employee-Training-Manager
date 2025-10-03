from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Certificate, Assignment


@receiver(post_delete, sender=Certificate)
def reset_assignment_status_on_delete(sender, instance, **kwargs):
    """
    When a certificate is deleted, reset the assignment status to PENDING.
    """
    try:
        assignment = Assignment.objects.get(employee=instance.user, course=instance.course)
        assignment.status = "PENDING"
        assignment.save()
    except Assignment.DoesNotExist:
        pass 


@receiver(post_save, sender=Certificate)
def mark_assignment_completed_on_upload(sender, instance, created, **kwargs):
    """
    When a certificate is uploaded, mark assignment as COMPLETED.
    """
    if created:
        try:
            assignment = Assignment.objects.get(employee=instance.user, course=instance.course)
            assignment.status = "COMPLETED"
            assignment.save()
        except Assignment.DoesNotExist:
            pass
