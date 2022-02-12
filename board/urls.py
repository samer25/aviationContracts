from django.urls import path

from rest_framework.routers import DefaultRouter

from board.views import RecruiterProfileAPIView, SeekerProfileAPIView, JobPostsViewSet

router = DefaultRouter()
router.register('recruiter', RecruiterProfileAPIView, basename='recruiter-profile')
router.register('seeker', SeekerProfileAPIView, basename='seeker-profile')
router.register('jobs', JobPostsViewSet, basename='job-posts')
urlpatterns = router.urls

# urlpatterns = [
#     path('recruiter-profile/', RecruiterProfileAPIView.as_view(), ),
#     path('seeker-profile/', SeekerProfileAPIView.as_view(),)
# ]
