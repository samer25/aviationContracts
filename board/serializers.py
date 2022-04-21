from rest_framework import serializers

from board.models import RecruiterProfileModel, SeekerProfileModel, JobPostsModel, ApplicantModel
from users.serializers import CustomUserSerializer


# class SubscriptionSerializer(serializers.ModelSerializer):
#     available_post = serializers.IntegerField(read_only=True)
#     plan_end_date = serializers.DateTimeField(read_only=True)
#
#     class Meta:
#         model = SubscriptionPlanModel
#         fields = ['id', 'membership', 'available_post', 'plan_end_date']


class RecruiterProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = CustomUserSerializer(read_only=True)

    # subscriptions = SubscriptionSerializer(read_only=True)

    class Meta:
        model = RecruiterProfileModel
        fields = ['id', 'user', 'profile_pic', 'company', 'position', 'phone_number']

    def create(self, validated_data):
        user = self.context['user']
        recruiter = RecruiterProfileModel(user=user, **validated_data)
        recruiter.save()
        return recruiter


class SeekerProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = SeekerProfileModel
        fields = ['id', 'user', 'about_me', 'phone_number', 'country', 'cv', 'is_open_to_work']

    def create(self, validated_data):
        user = self.context['user']
        seeker = SeekerProfileModel(user=user, **validated_data)
        seeker.save()
        return seeker


class JobPostsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = JobPostsModel
        fields = ['id', 'recruiter_id', 'position', 'location', 'location', 'salary', 'aircraft_type', 'sector',
                  'job_role',
                  'valid_till', 'organization', 'organization_logo', 'description', 'post_date', 'slug']
        lookup_field = 'slug'

    def create(self, validated_data):
        user_id = self.context['user'].id
        job = JobPostsModel(recruiter_id=user_id, **validated_data)
        job.save()
        return job


class CreateApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantModel
        fields = ['id', 'user_applied', 'job_post']


class ApplicantSerializer(serializers.ModelSerializer):
    user_applied = CustomUserSerializer(read_only=True)
    job_post = JobPostsSerializer(read_only=True)
    profile = SeekerProfileSerializer(read_only=True)

    class Meta:
        model = ApplicantModel
        fields = ['id', 'user_applied', 'profile', 'job_post']
