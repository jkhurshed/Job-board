"""
Test for job entity.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import datetime

from contents.models import Location

from employers.models import Company

from ..models import Job

from decimal import Decimal


class JobTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        self.location = Location.objects.create(
            address="Khujand Lincoln st. 1",
        )
        self.company = Company.objects.create(
            title="Sample company",
        )

    def test_job_create(self):
        job = Job.objects.create(
            owner=self.user,
            title='Sample title',
            description='Sample description',
            location=self.location,
            company=self.company,
            created_at=datetime.now(),
            salary=Decimal(5000.00),
        )
