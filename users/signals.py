from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Student, StudentProfile, Teacher, TeacherProfile, User


@receiver(post_save, sender=User)
@receiver(post_save, sender=Student)
@receiver(post_save, sender=Teacher)
def sync_student_profile(sender, instance, **kwargs):
    if instance.is_student:
        StudentProfile.objects.update_or_create(
            user=instance,
            defaults={"is_active": True},
        )
    else:
        StudentProfile.objects.filter(user=instance).update(is_active=False)


@receiver(post_save, sender=User)
@receiver(post_save, sender=Student)
@receiver(post_save, sender=Teacher)
def sync_teacher_profile(sender, instance, **kwargs):
    if instance.is_teacher:
        TeacherProfile.objects.update_or_create(
            user=instance,
            defaults={"is_active": True},
        )
    else:
        TeacherProfile.objects.filter(user=instance).update(is_active=False)
