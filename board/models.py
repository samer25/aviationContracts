import uuid

from django.conf import settings
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models

# Create your models here.
from django_countries.fields import CountryField
from social_core.utils import slugify

from core.settings import AUTH_USER_MODEL
from PIL import Image


def resizing_image(image):
    from PIL import Image

    img = Image.open(image.path)  # Open image
    # resize image
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)  # Resize image
        return img.save(image.path)  # Save it again and override the larger image


class RecruiterProfile(models.Model):
    MEMBERSHIP_NONE = 'N'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_NONE, 'NONE',),
        (MEMBERSHIP_SILVER, 'Silver',),
        (MEMBERSHIP_GOLD, 'GOLD',),

    ]

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    profile_pic = models.ImageField(upload_to='recruiter/profile_pic')
    company = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_NONE)
    available_post = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.membership == 'N':
            self.available_post = 3
        elif self.membership == 'S':
            self.available_post = 10
        elif self.membership == 'G':
            self.available_post = 50

        super().save(*args, **kwargs)

        resizing_image(self.profile_pic)


class SeekerProfile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='seeker/profile_pic')
    about_me = models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    country = CountryField(blank_label='(select country)')
    cv = models.FileField(upload_to='seeker/cv',
                          validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])], blank=True)
    is_open_to_work = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resizing_image(self.profile_pic)


class JobPosts(models.Model):
    recruiter = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=300)
    location = CountryField(blank_label='(select country)')
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
