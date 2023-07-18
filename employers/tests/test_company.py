"""
Testing location entity
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Company
from contents.models import Location


class CompanyTest(TestCase):
    """Test model"""

    def setUp(self):
        self.image = SimpleUploadedFile(
            "test_image.jpg",
            b"image_content",
            content_type="image/jpeg"
        )

    def test_create_company(self):
        """Creating a Company successful"""
        company_location = Location.objects.create(
            address="TestCity st. test1",
        )
        self.company = Company.objects.create(
            title="Sample title",
            description="Sample description",
            website="https://example.com",
            logo=self.image,
            location=company_location,
        )

        self.assertEqual(str(self.company), self.company.title)

    def tearDown(self):
        self.company.logo.delete()
