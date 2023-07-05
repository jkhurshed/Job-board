from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from contents.models import Location
from ..serializers import LocationSerializer

LOCATION_URL = reverse("contents:location-list")


def detail_url(location_id):
    """Create and return a recipe detail URL."""
    return reverse('contents:location-detail', args=[location_id])


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


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicLocationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(LOCATION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLocationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_locations(self):

        create_location()
        # create_category()

        res = self.client.get(LOCATION_URL)

        location = Location.objects.all().order_by('country')
        serializer = LocationSerializer(location, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_location_detail(self):
        location = create_location()

        url = detail_url(location.id)
        res = self.client.get(url)

        serializer = LocationSerializer(location)
        self.assertEqual(res.data, serializer.data)

    def test_create_location(self):
        """Test creating a location."""
        payload = {
            "country": "Tajikistan",
            "state": "Sugd",
            "city": "Khujand",
            "address": "Lincoln st. 2",
        }
        res = self.client.post(LOCATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        location = Location.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(location, k), v)

    def test_partial_update(self):
        location = create_location(
            country="Tajikistan",
            state="Sugd",
            city="Khujand",
            address="Lincoln st. 2",
        )

        payload = {
            "country": "Tajikistan",
            "state": "Sugd",
            "city": "Khujand",
            "address": "Lincoln st. 2",
        }
        url = detail_url(location.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        location.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(location, k), v)

    def test_delete_location(self):
        """Test deleting a category successful"""
        location = create_location()

        url = detail_url(location.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Location.objects.filter(id=location.id).exists())
