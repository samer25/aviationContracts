from django.urls import path

from rest_framework.routers import DefaultRouter

from board.views import RecruiterProfileAPIView, SeekerProfileAPIView

router = DefaultRouter()
router.register('recruiter', RecruiterProfileAPIView, basename='recruiter-profile')
router.register('seeker', SeekerProfileAPIView, basename='seeker-profile')

urlpatterns = router.urls

# urlpatterns = [
#     path('recruiter-profile/', RecruiterProfileAPIView.as_view(), ),
#     path('seeker-profile/', SeekerProfileAPIView.as_view(),)
# ]
