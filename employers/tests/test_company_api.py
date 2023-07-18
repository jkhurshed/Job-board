"""
Tests for company api, testing crud operations and others.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Company
from contents.models import Location
from ..serializers import CompanySerializer


COMPANY_URL = reverse("employers:company-list")


def detail_url(company_id):
    """Create and return a recipe detail URL."""
    return reverse('employers:company-detail', args=[company_id])


def create_company(**params):
    location = Location.objects.create(address="Test Address")
    image = SimpleUploadedFile(
        "test_image.jpg",
        b"image_content",
        content_type="image/jpeg"
    )

    defaults = {
        "title": "Sample Company",
        "description": "Sample description",
        "website": "http://example.com",
        "logo": image,
        "location": location,
    }
    defaults.update(params)

    company = Company.objects.create(**defaults)

    return company


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicCompanyAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(COMPANY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCompanyApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_company(self):
        """Test for retrieving company"""
        create_company()

        res = self.client.get(COMPANY_URL)

        company = Company.objects.all().order_by('id')
        serializer = CompanySerializer(company, many=True)

        expected_data = serializer.data
        for item in expected_data:
            item['logo'] = f"http://testserver{item['logo']}"
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_get_company_detail(self):
        """Test get company detail"""
        company = create_company()

        url = detail_url(company.id)
        res = self.client.get(url)

        serializer = CompanySerializer(company)

        expected_data = serializer.data
        expected_data['logo'] = f"http://testserver{expected_data['logo']}"

        self.assertEqual(res.data, expected_data)

    def test_create_company(self):
        """Test creating a company."""
        self.location = Location.objects.create(address="Test Address")
        location_uuid = str(self.location.id)
        payload = {
            "title": "Sample Company",
            "description": "Sample description",
            "website": "http://example.com",
            "location": location_uuid,
        }
        res = self.client.post(COMPANY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        company = Company.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if k == 'location':
                self.assertEqual(location_uuid, v)
            else:
                self.assertEqual(getattr(company, k), v)

    def test_delete_company(self):
        """Test deleting a company successful"""
        company = create_company()

        url = detail_url(company.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(id=company.id).exists())
