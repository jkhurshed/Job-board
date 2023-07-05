"""
Testing location entity
"""
import os
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

    def tearDown(self):
        for objects in Company.objects.all():
            if objects.logo:
                path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    '../../images',
                    os.path.basename(objects.logo.path)
                )
                os.remove(path)
                # print(f"Deleted image: {path}")

    def test_create_company(self):
        """Creating a Company successful"""
        company_location = Location.objects.create(
            address="TestCity st. test1",
        )
        company = Company.objects.create(
            title="Sample title",
            description="Sample description",
            website="https://example.com",
            logo=self.image,
            location=company_location,
        )

        self.assertEqual(str(company), company.title)
