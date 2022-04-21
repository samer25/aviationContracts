from rest_framework_nested import routers
from board.views import RecruiterProfileAPIViewSet, SeekerProfileAPIViewSet, JobPostsAPIViewSet, ApplicantAPIViewSet

router = routers.DefaultRouter()
router.register('recruiter', RecruiterProfileAPIViewSet, basename='recruiter-profile')
router.register('seeker', SeekerProfileAPIViewSet, basename='seeker-profile')
router.register('jobs', JobPostsAPIViewSet, basename='job-posts')
router.register('applicant', ApplicantAPIViewSet, basename='applicant')

# sub = routers.NestedDefaultRouter(router, 'recruiter', lookup='recruiter')
# sub.register('subscription', SubscriptionAPIViewSet, basename='subscription')
urlpatterns = router.urls

