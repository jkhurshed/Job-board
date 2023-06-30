from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from contents.models import Location
from ..serializers import LocationSerializer

LOCATION_URL = reverse("contents:location-list")


def create_location(**params):

    defaults = {
        "country": "Tajikistan",
        "state": "Sugd",
        "city": "Khujand",
        "address": "Lincoln st. 2",
    }
    defaults.update(params)

    location = Location.objects.create(**defaults)
    return location


class PublicLocationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(LOCATION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLocationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword',
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_locations(self):

        create_location()
        # create_category()

        res = self.client.get(LOCATION_URL)

        location = Location.objects.all().order_by('country')
        serializer = LocationSerializer(location, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
