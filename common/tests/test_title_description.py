"""
Testing category entity
"""
from django.test import TestCase

from ..models import BaseModel


class CategoryTest(TestCase):
    """Test model"""
    def create_category(self):
        """Creating a category successful"""
        base_model = BaseModel.objects.create(

            title="Sample category title",
            description="Sample description",
        )

        self.assertEqual(str(base_model), base_model.title)
