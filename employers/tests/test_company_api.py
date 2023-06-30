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
        # "logo": image,
        "location": location,
    }
    defaults.update(params)

    company = Company.objects.create(**defaults)
    return company


class PublicCompanyAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(COMPANY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCompanyApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword',
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_company(self):
        create_company()

        res = self.client.get(COMPANY_URL)

        skills = Company.objects.all().order_by('id')
        serializer = CompanySerializer(skills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
