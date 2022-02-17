from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from board.models import RecruiterProfile, SeekerProfile, JobPosts
from board.serializers import RecruiterProfileSerializer, SeekerProfileSerializer, JobPostsSerializer


class RecruiterProfileAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = RecruiterProfile.objects.select_related('user').all()
    serializer_class = RecruiterProfileSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        profile = get_object_or_404(RecruiterProfile, user_id=request.user.id)
        if request.method == 'GET':
            serializer = RecruiterProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = RecruiterProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SeekerProfileAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SeekerProfile.objects.select_related('user').all()
    serializer_class = SeekerProfileSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        profile = get_object_or_404(SeekerProfile, user_id=request.user.id)
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
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {'user': self.request.user}

    def create(self, request, *args, **kwargs):
        available = request.user.recruiter_profile.available_post
        current_posts_count = self.queryset.filter(recruiter=request.user).count()
        if current_posts_count < available:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('User membership does not allow to create more job posts',
                            status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['GET', 'PUT', 'DELETE'])
    def my(self, request):
        posts = JobPosts.objects.filter(recruiter_id=request.user.id).all()

        if request.method == 'GET':
            serializer = JobPostsSerializer(posts, many=True)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = JobPostsSerializer(posts, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            posts.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
