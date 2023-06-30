"""
Testing location entity
"""
# from django.test import TestCase
# from django.core.files.uploadedfile import SimpleUploadedFile
#
# from ..models import Company
# from contents.models import Location
#
#
# class CompanyTest(TestCase):
#     """Test model"""
#     def test_create_company(self):
#         """Creating a Company successful"""
#         company_location = Location.objects.create(
#             address="TestCity st. test1",
#         )
#         image = SimpleUploadedFile(
#             "test_image.jpg",
#             b"image_content",
#             content_type="image/jpeg"
#         )
#         company = Company.objects.create(
#             title="Sample title",
#             description="Sample description",
#             website="https://example.com",
#             logo=image,
#             location=company_location,
#         )
#
#         self.assertEqual(str(company), company.title)
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from ..models import Company
from contents.models import Location


class CompanyTest(TestCase):
    """Test model"""

    def test_create_company_with_mocked_image(self):
        """Creating a Company successfully with mocked image"""

        company_location = Location.objects.create(
            address="TestCity st. test1",
        )

        # Mock the image upload process
        with patch('django.core.files.storage.FileSystemStorage.save') as mock_save:
            mock_save.return_value = 'images/test_image.jpg'

            company = Company.objects.create(
                title="Sample title",
                description="Sample description",
                website="https://example.com",
                logo=SimpleUploadedFile(
                    "test_image.jpg",
                    b"image_content",
                    content_type="image/jpeg"
                ),
                location=company_location,
            )

            self.assertEqual(str(company), company.title)
            self.assertEqual(company.logo.name, 'images/test_image.jpg')

            # Assert that the save method was called once with the expected arguments
            mock_save.assert_called_once()
