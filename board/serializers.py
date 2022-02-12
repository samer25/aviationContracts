from rest_framework import serializers

from board.models import RecruiterProfile, SeekerProfile, JobPosts


class RecruiterProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = ['id', 'user_id', 'company', 'position', 'phone_number', 'member_ship']


class SeekerProfileSerializer(serializers.ModelSerializer):
    recruiter_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SeekerProfile
        fields = ['id', 'recruiter_id', 'about_me', 'phone_number', 'country', 'cv', 'is_open_to_work']


class JobPostsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = JobPosts
        fields = ['id', 'user_id', 'position', 'location', 'location', 'aircraft_type', 'sector', 'job_role',
                  'valid_till', 'organization', 'organization_logo', 'description', 'post_date']
