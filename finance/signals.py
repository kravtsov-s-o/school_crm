import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from companies.models import Company
from finance.models import Account, Transaction
from users.models import StudentProfile, TeacherProfile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Company)
@receiver(post_save, sender=TeacherProfile)
@receiver(post_save, sender=StudentProfile)
def create_account(sender, instance, created, **kwargs):
    if instance.account_id is None:
        instance.account = Account.objects.create()
        instance.save(update_fields=["account"])


@receiver(post_save, sender=Transaction)
def log_transaction(sender, instance, created, **kwargs):
    if created:
        logger.info(
            "transaction #%s account=%s type=%s amount=%s lesson=%s",
            instance.pk, instance.account_id, instance.type,
            instance.amount, instance.lesson_id,
        )
