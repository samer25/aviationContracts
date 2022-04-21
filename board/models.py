import uuid

from django.conf import settings
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models

from social_core.utils import slugify


def resizing_image(image):
    from PIL import Image
    img = Image.open(image.path)  # Open image
    # resize image
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)  # Resize image
        return img.save(image.path)  # Save it again and override the larger image


class RecruiterProfileModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    profile_pic = models.ImageField(upload_to='recruiter/profile_pic', null=True, blank=True)
    company = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.profile_pic)
        resizing_image(self.profile_pic)


class SeekerProfileModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='seeker/profile_pic')
    about_me = models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    country = models.CharField(max_length=255)
    cv = models.FileField(upload_to='seeker/cv',
                          validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])], blank=True)
    is_open_to_work = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resizing_image(self.profile_pic)


class JobPostsModel(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=300)
    location = models.CharField(max_length=255)
    salary = models.BigIntegerField(blank=True, null=True)
    aircraft_type = models.CharField(max_length=255, blank=True)  # '(boeing, airbus ...)'
    sector = models.CharField(max_length=255, blank=True)  # '(aircraft, flight crew ...)'
    job_role = models.CharField(max_length=255, blank=True)  # '(engineers jobs, office jobs ...)'
    valid_till = models.DateField(blank=True)
    organization = models.CharField(max_length=255, blank=True)
    organization_logo = models.ImageField(upload_to='recruiter/organization_logo')
    description = models.TextField(blank=True)
    post_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    job_creation_id = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)

    class Meta:
        ordering = ('-post_date',)

    def __str__(self):
        return self.position

    def save(self, *args, **kwargs):
        self.job_creation_id = uuid.uuid1()
        self.slug = slugify(f'{self.job_creation_id}-{self.position}')
        super().save(*args, **kwargs)
        resizing_image(self.organization_logo)


class ApplicantModel(models.Model):
    user_applied = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seeker_applied')
    job_post = models.ForeignKey(JobPostsModel, on_delete=models.CASCADE, related_name='job_applied')
