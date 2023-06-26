"""
Testing location entity
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Company
from contents.models import Location


class CompanyTest(TestCase):
    """Test model"""
    def test_create_company(self):
        """Creating a Company successful"""
        company_location = Location.objects.create(
            address="TestCity st. test1",
        )
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"image_content",
            content_type="image/jpeg"
        )
        company = Company.objects.create(
            title="Sample title",
            description="Sample description",
            website="https://example.com",
            logo=image,
            location=company_location,
        )

        self.assertEqual(str(company), company.title)
