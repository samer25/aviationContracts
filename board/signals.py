from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from board.models import RecruiterProfileModel, JobPostsModel, SeekerProfileModel
from users.models import CustomUser


@receiver(post_save, sender=RecruiterProfileModel)
def update_user_is_recruiter_if_recruiter_profile_is_created(sender, **kwargs):
    if kwargs['created']:
        CustomUser.objects.update(is_recruiter=True)


@receiver(post_delete, sender=SeekerProfileModel)
@receiver(post_delete, sender=RecruiterProfileModel)
def photo_post_delete_handler(sender, **kwargs):
    recruiter = kwargs['instance']

    if recruiter.profile_pic:
        storage, path = recruiter.profile_pic.storage, recruiter.profile_pic.path
        storage.delete(path)


@receiver(post_delete, sender=SeekerProfileModel)
def photo_post_delete_handler(sender, **kwargs):
    seeker = kwargs['instance']
    if seeker.cv:
        storage, path = seeker.cv.storage, seeker.cv.path
        storage.delete(path)


@receiver(post_delete, sender=JobPostsModel)
def photo_post_delete_handler(sender, **kwargs):
    job = kwargs['instance']
    if job.organization_logo:
        storage, path = job.organization_logo.storage, job.organization_logo.path
        storage.delete(path)


@receiver(pre_save, sender=RecruiterProfileModel)
@receiver(pre_save, sender=SeekerProfileModel)
def delete_profile_pic_on_change_extension(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_profile_pic = SeekerProfileModel.objects.get(pk=instance.pk).profile_pic
        except SeekerProfileModel.DoesNotExist or RecruiterProfileModel.DoesNotExist:
            return
        else:
            new_profile_pic = instance.profile_pic
            if old_profile_pic and old_profile_pic.url != new_profile_pic.url:
                old_profile_pic.delete(save=False)


@receiver(pre_save, sender=SeekerProfileModel)
def delete_cv_on_change_extension(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_cv = SeekerProfileModel.objects.get(pk=instance.pk).cv
        except SeekerProfileModel.DoesNotExist:
            return
        else:
            new_cv = instance.profile_pic
            if old_cv and old_cv.url != new_cv.url:
                old_cv.delete(save=False)


@receiver(pre_save, sender=JobPostsModel)
def delete_organization_logo_on_change_extension(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_organization_logo = JobPostsModel.objects.get(pk=instance.pk).organization_logo
        except JobPostsModel.DoesNotExist:
            return
        else:
            new_organization_logo = instance.organization_logo
            if old_organization_logo and old_organization_logo.url != new_organization_logo.url:
                old_organization_logo.delete(save=False)
