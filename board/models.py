from django.conf import settings
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models

# Create your models here.
from django_countries.fields import CountryField

from core.settings import AUTH_USER_MODEL


class RecruiterProfile(models.Model):
    MEMBERSHIP_NONE = 'N'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_NONE, 'NONE',),
        (MEMBERSHIP_SILVER, 'Silver',),
        (MEMBERSHIP_GOLD, 'GOLD',),

    ]

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    member_ship = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_NONE)


class SeekerProfile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    about_me = models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    country = CountryField(blank_label='(select country)')
    cv = models.FileField(upload_to='seeker/cv',
                          validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])], blank=True)
    is_open_to_work = models.BooleanField(default=True)


class JobPosts(models.Model):
    recruiter = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=300)
    location = CountryField(blank_label='(select country)')
    salary = models.BigIntegerField(blank=True)
    aircraft_type = models.CharField(max_length=255, blank=True)  # '(boeing, airbus ...)'
    sector = models.CharField(max_length=255, blank=True)  # '(aircraft, flight crew ...)'
    job_role = models.CharField(max_length=255, blank=True)  # '(engineers jobs, office jobs ...)'
    valid_till = models.DateField(blank=True)
    organization = models.CharField(max_length=255, blank=True)
    organization_logo = models.ImageField(upload_to='recruiter/organization_logo')
    description = models.TextField(blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
