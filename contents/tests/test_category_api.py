from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from contents.models import Category

from ..serializers import CategorySerializer

CATEGORY_URL = reverse("contents:category-list")


def create_category(**params):

    defaults = {
        "title": "Sample category title",
        "description": "Sample category description",
    }
    defaults.update(params)

    category = Category.objects.create(**defaults)
    return category


class PublicCategoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword',
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_categories(self):

        create_category()
        # create_category()

        res = self.client.get(CATEGORY_URL)

        category = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(category, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
