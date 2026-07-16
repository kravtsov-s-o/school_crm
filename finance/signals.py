from django.db.models.signals import post_save
from django.dispatch import receiver

from companies.models import Company
from finance.models import Account
from users.models import StudentProfile, TeacherProfile


@receiver(post_save, sender=Company)
@receiver(post_save, sender=TeacherProfile)
@receiver(post_save, sender=StudentProfile)
def create_account(sender, instance, created, **kwargs):
    if instance.account_id is None:
        instance.account = Account.objects.create()
        instance.save(update_fields=["account"])
