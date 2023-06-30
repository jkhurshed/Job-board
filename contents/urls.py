from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, LocationViewSet, SKillViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('location', LocationViewSet)
router.register('skill', SKillViewSet)

app_name = 'contents'

urlpatterns = [
    path('', include(router.urls)),
]
