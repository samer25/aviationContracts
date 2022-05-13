from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from board.models import RecruiterProfileModel, SeekerProfileModel, JobPostsModel, ApplicantModel
from board.permissions import IsRecruiterOrReadOnly
from board.serializers import RecruiterProfileSerializer, SeekerProfileSerializer, JobPostsSerializer, \
    ApplicantSerializer, CreateApplicantSerializer


class RecruiterProfileAPIViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                                 GenericViewSet):
    queryset = RecruiterProfileModel.objects.select_related('user').all().order_by('id')
    serializer_class = RecruiterProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        profile = get_object_or_404(self.queryset, user_id=request.user.id)
        if request.method == 'GET':
            serializer = RecruiterProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = RecruiterProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def my_jobs(self, request):
        posts = JobPostsModel.objects.filter(recruiter_id=request.user.id).all()

        if request.method == 'GET':
            serializer = JobPostsSerializer(posts, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def my_jobs_users_applied(self, request):
        posts = ApplicantModel.objects.select_related('job_post').select_related('user_applied').filter(
            job_post__recruiter_id=request.user.id).all()
        serializer = ApplicantSerializer(posts, many=True)
        return Response(serializer.data)


class SeekerProfileAPIViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SeekerProfileModel.objects.select_related('user').all()
    serializer_class = SeekerProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    def me_applied_jobs(self, request):
        applied = ApplicantModel.objects.select_related('job_post').select_related('user_applied').filter(
            user_applied_id=request.user.id).all()
        serializer = ApplicantSerializer(applied, many=True)
        return Response(serializer.data)


class JobPostsAPIViewSet(ModelViewSet):
    queryset = JobPostsModel.objects.all()
    serializer_class = JobPostsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['position', 'location', 'aircraft_type', 'salary']
    lookup_field = 'slug'
    permission_classes = [IsRecruiterOrReadOnly]

    def get_serializer_context(self):
        return {'user': self.request.user}


class ApplicantAPIViewSet(CreateModelMixin, GenericViewSet):
    queryset = ApplicantModel.objects.all()
    serializer_class = CreateApplicantSerializer

    def create(self, request, *args, **kwargs):
        is_applied = self.queryset.filter(user_applied=request.data['user_applied'], job_post=request.data['job_post'])
        if is_applied:
            return Response('The user already applied', status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
