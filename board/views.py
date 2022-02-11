from django.contrib.admin import actions
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet

from board.models import RecruiterProfile, SeekerProfile
from board.serializers import RecruiterProfileSerializer, SeekerProfileSerializer
from users.models import CustomUser


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
