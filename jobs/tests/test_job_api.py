"""
Tests for job api, testing crud operations and others.
"""
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
    """Tests for testing CRUD operations for authenticated users."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_job(self):
        """Test for retrieving job APIs"""
        create_job(user=self.user)

        res = self.client.get(JOB_URL)

        company = Job.objects.all().order_by('id')
        serializer = JobSerializer(company, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_job_detail(self):
        """Test for getting jobs detail"""
        job = create_job(user=self.user)

        url = detail_url(job.id)
        res = self.client.get(url)

        serializer = JobDetailSerializer(job)

        self.assertEqual(res.data, serializer.data)

    def test_create_job(self):
        """Test creating a company."""
        self.location = Location.objects.create(address="Test Address")
        self.company = Company.objects.create(title="Sample company", location=self.location)

        location_uuid = str(self.location.id)
        company_uuid = str(self.company.id)

        payload = {
            "user": self.user,
            "title": 'Sample title',
            "description": 'Sample description',
            "location": location_uuid,
            "company": company_uuid,
            "created_at": datetime.now(),
            "salary": Decimal(50.00),
        }
        res = self.client.post(JOB_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        job = Job.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if payload['location']:
                self.assertEqual(location_uuid, payload['location'])
            if payload['company']:
                self.assertEqual(company_uuid, payload['company'])
            else:
                self.assertEqual(getattr(job, k), v)

    def test_partial_update(self):
        """Test for partial jobs updating"""
        self.location = Location.objects.create(address="Test Address")
        self.company = Company.objects.create(title="Sample company", location=self.location)

        location_uuid = str(self.location.id)
        company_uuid = str(self.company.id)

        job = create_job(user=self.user)

        payload = {
            "title": 'Sample title',
            "description": 'Sample description',
            "location": location_uuid,
            "company": company_uuid,
            "created_at": datetime.now(),
            "salary": Decimal(50.00),
        }
        url = detail_url(job.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        job.refresh_from_db()
        for k, v in payload.items():
            if payload['location']:
                self.assertEqual(location_uuid, payload['location'])
            if payload['company']:
                self.assertEqual(company_uuid, payload['company'])
            else:
                self.assertEqual(getattr(job, k), v)

    def test_update_user_returns_error(self):
        new_user = create_user(email="user2@example.com", password='test123')
        job = create_job(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(job.id)
        self.client.put(url, payload)

        job.refresh_from_db()
        self.assertEqual(job.user, self.user)

    def test_delete_job(self):
        """Test deleting a job successful"""
        job = create_job(user=self.user)

        url = detail_url(job.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Job.objects.filter(id=job.id).exists())


class JobFilterTestCase(TestCase):
    """Tests for jobs filtering"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)

        # self.location1 = Location.objects.create(city='New York')
        # self.location2 = Location.objects.create(city='San Francisco')
        # self.location3 = Location.objects.create(city='Seattle')

    def test_job_filtering_by_title(self):
        """Test for filtering job by title"""
        create_job(user=self.user)
        payload = {
            'title': 'Sample title'
        }
        res = self.client.get(JOB_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'Sample title')

    def test_job_filtering_by_location(self):
        """Test for filtering job by the location"""
        location = Location.objects.create(city="San Fransisco")
        location_id = str(location.id)
        create_job(user=self.user, location=location)
        payload = {
            'location': location_id
        }
        res = self.client.get(JOB_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(str(res.data[0]['location']), location_id)
