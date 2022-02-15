import os

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from board.models import RecruiterProfile, JobPosts, SeekerProfile
from users.models import CustomUser


@receiver(post_save, sender=RecruiterProfile)
def update_user_is_recruiter_if_recruiter_profile_is_created(sender, **kwargs):
    if kwargs['created']:
        CustomUser.objects.update(is_recruiter=True)


@receiver(post_delete, sender=SeekerProfile)
@receiver(post_delete, sender=RecruiterProfile)
def photo_post_delete_handler(sender, **kwargs):
    recruiter = kwargs['instance']

    if recruiter.profile_pic:
        storage, path = recruiter.profile_pic.storage, recruiter.profile_pic.path
        storage.delete(path)


@receiver(post_delete, sender=SeekerProfile)
def photo_post_delete_handler(sender, **kwargs):
    seeker = kwargs['instance']
    if seeker.cv:
        storage, path = seeker.cv.storage, seeker.cv.path
        storage.delete(path)


@receiver(post_delete, sender=JobPosts)
def photo_post_delete_handler(sender, **kwargs):
    job = kwargs['instance']
    if job.organization_logo:
        storage, path = job.organization_logo.storage, job.organization_logo.path
        storage.delete(path)


@receiver(pre_save, sender=RecruiterProfile)
@receiver(pre_save, sender=SeekerProfile)
def delete_profile_pic_on_change_extension(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_profile_pic = SeekerProfile.objects.get(pk=instance.pk).profile_pic
        except SeekerProfile.DoesNotExist or RecruiterProfile.DoesNotExist:
            return
        else:
            new_profile_pic = instance.profile_pic
            if old_profile_pic and old_profile_pic.url != new_profile_pic.url:
                old_profile_pic.delete(save=False)


@receiver(pre_save, sender=SeekerProfile)
def delete_cv_on_change_extension(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_cv = SeekerProfile.objects.get(pk=instance.pk).cv
        except SeekerProfile.DoesNotExist:
            return
        else:
            new_cv = instance.profile_pic
            if old_cv and old_cv.url != new_cv.url:
                old_cv.delete(save=False)


@receiver(pre_save, sender=JobPosts)
def delete_organization_logo_on_change_extension(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_organization_logo = JobPosts.objects.get(pk=instance.pk).organization_logo
        except JobPosts.DoesNotExist:
            return
        else:
            new_organization_logo = instance.organization_logo
            if old_organization_logo and old_organization_logo.url != new_organization_logo.url:
                old_organization_logo.delete(save=False)
