from django.contrib import admin

# Register your models here.
from board.models import RecruiterProfile, SeekerProfile, JobPosts

admin.site.register(RecruiterProfile)
admin.site.register(SeekerProfile)
admin.site.register(JobPosts)