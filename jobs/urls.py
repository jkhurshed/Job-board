from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import JobViewSet, ApplicantViewSet

router = DefaultRouter()
router.register('job', JobViewSet)
router.register('applicant', ApplicantViewSet)

app_name = 'jobs'

urlpatterns = [
    path('', include(router.urls)),
]
