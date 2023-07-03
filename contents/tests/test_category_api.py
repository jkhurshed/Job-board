from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from contents.models import Category

from ..serializers import CategorySerializer, CategoryDetailSerializer

CATEGORY_URL = reverse("contents:category-list")


def detail_url(category_id):
    """Create and return a recipe detail URL."""
    return reverse('contents:category-detail', args=[category_id])


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

    def test_get_category_detail(self):
        category = create_category()

        url = detail_url(category.id)
        res = self.client.get(url)

        serializer = CategoryDetailSerializer(category)
        self.assertEqual(res.data, serializer.data)

    def test_create_category(self):
        """Test creating a recipe."""
        payload = {
            "title": "Sample category",
            "description": "Sample description",
        }
        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(category, k), v)
