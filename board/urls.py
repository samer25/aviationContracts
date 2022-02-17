from django.urls import path

from rest_framework.routers import DefaultRouter

from board.views import RecruiterProfileAPIViewSet, SeekerProfileAPIViewSet, JobPostsAPIViewSet, ApplicantAPIViewSet

router = DefaultRouter()
router.register('recruiter', RecruiterProfileAPIViewSet, basename='recruiter-profile')
router.register('seeker', SeekerProfileAPIViewSet, basename='seeker-profile')
router.register('jobs', JobPostsAPIViewSet, basename='job-posts')
router.register('applicant', ApplicantAPIViewSet, basename='applicant')
urlpatterns = router.urls

# urlpatterns = [
#     path('recruiter-profile/', RecruiterProfileAPIView.as_view(), ),
#     path('seeker-profile/', SeekerProfileAPIView.as_view(),)
# ]
