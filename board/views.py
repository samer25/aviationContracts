from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from board.models import RecruiterProfile, SeekerProfile, JobPosts, Applicant
from board.serializers import RecruiterProfileSerializer, SeekerProfileSerializer, JobPostsSerializer, \
    ApplicantSerializer, CreateApplicantSerializer


class RecruiterProfileAPIViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                                 GenericViewSet):
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


class SeekerProfileAPIViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SeekerProfile.objects.select_related('user').all()
    serializer_class = SeekerProfileSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        profile = get_object_or_404(self.queryset, user_id=request.user.id)
        if request.method == 'GET':
            serializer = SeekerProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = SeekerProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def job_applied(self, request):
        applied = Applicant.objects.select_related('job_post').select_related('user').filter(
            user_id=request.user.id).all()
        serializer = ApplicantSerializer(applied, many=True)
        return Response(serializer.data)


class JobPostsAPIViewSet(ModelViewSet):
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

    @action(detail=False, methods=['GET'])
    def my_jobs(self, request):
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

    @action(detail=False, methods=['GET'])
    def user_applied(self, request):
        posts = Applicant.objects.select_related('job_post').select_related('user').filter(
            job_post__recruiter_id=request.user.id).all()
        serializer = ApplicantSerializer(posts, many=True)
        return Response(serializer.data)


class ApplicantAPIViewSet(CreateModelMixin, GenericViewSet):
    queryset = Applicant.objects.all()
    serializer_class = CreateApplicantSerializer

    def create(self, request, *args, **kwargs):
        is_applied = self.queryset.filter(user=request.data['user'], job_post=request.data['job_post'])
        if is_applied:
            return Response('The user already applied')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
