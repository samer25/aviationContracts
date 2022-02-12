from django.contrib.admin import actions
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from board.models import RecruiterProfile, SeekerProfile, JobPosts
from board.serializers import RecruiterProfileSerializer, SeekerProfileSerializer, JobPostsSerializer


class RecruiterProfileAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = RecruiterProfile.objects.all()
    serializer_class = RecruiterProfileSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        profile = RecruiterProfile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = RecruiterProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = RecruiterProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SeekerProfileAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SeekerProfile.objects.all()
    serializer_class = SeekerProfileSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        profile = SeekerProfile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = SeekerProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = SeekerProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobPostsViewSet(ModelViewSet):
    queryset = JobPosts.objects.all()
    serializer_class = JobPostsSerializer

    @action(detail=False, methods=['GET', 'PUT', 'DELETE'])
    def my(self, request):
        posts = JobPosts.objects.get(recruiter_id=request.user.id)
        if request.method == 'GET':
            serializer = JobPostsSerializer(posts)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = JobPostsSerializer(posts, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            posts.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
