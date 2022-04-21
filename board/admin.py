from django.contrib import admin

# Register your models here.
from board.models import RecruiterProfileModel, SeekerProfileModel, JobPostsModel, ApplicantModel

admin.site.register(RecruiterProfileModel)
admin.site.register(SeekerProfileModel)
admin.site.register(JobPostsModel)
admin.site.register(ApplicantModel)
# admin.site.register(SubscriptionPlanModel)
