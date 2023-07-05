from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Job
from contents.models import Location
from employers.models import Company
from ..serializers import JobSerializer, JobDetailSerializer

from datetime import datetime
from decimal import Decimal

JOB_URL = reverse("jobs:job-list")


def detail_url(job_id):
    """Create and return a recipe detail URL."""
    return reverse('jobs:job-detail', args=[job_id])


def create_job(user, **params):
    location = Location.objects.create(address="Test Address")
    company = Company.objects.create(title="Sample company", location=location)
    defaults = {
        "title": 'Sample title',
        "description": 'Sample description',
        "location": location,
        "company": company,
        "created_at": datetime.now(),
        "salary": Decimal(50.00),
    }
    defaults.update(params)

    job = Job.objects.create(user=user, **defaults)

    return job


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicJobAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(JOB_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJobApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_company(self):
        create_job(user=self.user)

        res = self.client.get(JOB_URL)

        company = Job.objects.all().order_by('id')
        serializer = JobSerializer(company, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_job_detail(self):
        job = create_job(user=self.user)

        url = detail_url(job.id)
        res = self.client.get(url)

        serializer = JobDetailSerializer(job)

        self.assertEqual(res.data, serializer.data)

    def test_create_job(self):
        """Test creating a company."""
        self.location = Location.objects.create(address="Test Address")
        self.company = Company.objects.create(title="Sample company", location=self.location)
        payload = {
            "title": 'Sample title',
            "description": 'Sample description',
            "location": self.location,
            "company": self.company,
            "created_at": datetime.now(),
            "salary": Decimal(50.00),
        }
        res = self.client.post(JOB_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        job = Job.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(job, k), v)
