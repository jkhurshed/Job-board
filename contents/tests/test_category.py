"""
Testing category entity
"""
from django.test import TestCase

from ..models import Category


class CategoryTest(TestCase):
    """Test model"""
    def test_create_category(self):
        """Creating a category successful"""
        category = Category.objects.create(

            title="Sample category title",
            description="Sample description",
        )

        self.assertEqual(str(category), category.title)
