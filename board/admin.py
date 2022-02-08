from django.contrib import admin

# Register your models here.
from board.models import RecruiterProfile, SeekerProfile

admin.site.register(RecruiterProfile)
admin.site.register(SeekerProfile)
