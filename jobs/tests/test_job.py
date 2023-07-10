"""
Tests for job entity.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from datetime import datetime

from contents.models import Location

from employers.models import Company

from ..models import Job

from decimal import Decimal


class JobTest(TestCase):
    """Test for creating job successfully"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        self.location = Location.objects.create(
            address="Khujand Lincoln st. 1",
        )
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"image_content",
            content_type="image/jpeg"
        )
        self.company = Company.objects.create(
            title="Sample title",
            description="Sample description",
            website="https://example.com",
            logo=image,
            location=self.location,
        )

    def test_job_create(self):
        """Creating job"""
        job = Job.objects.create(
            user=self.user,
            title='Sample title',
            description='Sample description',
            location=self.location,
            company=self.company,
            created_at=datetime.now(),
            salary=Decimal(50.00),
        )

        self.assertEqual(job.user, self.user)
        self.assertEqual(job.title, 'Sample title')
        self.assertEqual(job.description, 'Sample description')
        self.assertEqual(job.location, self.location)
        self.assertEqual(job.company, self.company)
        self.assertEqual(job.salary, Decimal('50.00'))
