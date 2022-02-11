from rest_framework import serializers

from board.models import RecruiterProfile, SeekerProfile


class RecruiterProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = ['id', 'user_id', 'company', 'position', 'phone_number', 'member_ship']


class SeekerProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SeekerProfile
        fields = ['id', 'user_id', 'about_me', 'phone_number', 'country', 'cv', 'is_open_to_work']
