from rest_framework import serializers

from board.models import RecruiterProfile, SeekerProfile, JobPosts
from users.serializers import CustomUserSerializer


class RecruiterProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = ['id', 'user', 'company', 'position', 'phone_number', 'member_ship']

    def create(self, validated_data):
        user = self.context['user']
        recruiter = RecruiterProfile(user=user, **validated_data)
        recruiter.save()
        return recruiter


class SeekerProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = SeekerProfile
        fields = ['id', 'user', 'about_me', 'phone_number', 'country', 'cv', 'is_open_to_work']

    def create(self, validated_data):
        user = self.context['user']
        seeker = SeekerProfile(user=user, **validated_data)
        seeker.save()
        return seeker


class JobPostsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = JobPosts
        fields = ['id', 'recruiter_id', 'position', 'location', 'location', 'salary', 'aircraft_type', 'sector',
                  'job_role',
                  'valid_till', 'organization', 'organization_logo', 'description', 'post_date', 'slug']
        lookup_field = 'slug'

    def create(self, validated_data):
        user_id = self.context['user'].id
        job = JobPosts(recruiter_id=user_id, **validated_data)
        job.save()
        return job

