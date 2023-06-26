"""
Testing location entity
"""
from django.test import TestCase

from ..models import Location


class LocationTest(TestCase):
    """Test model"""
    def test_create_location(self):
        """Creating a location successful"""
        location = Location.objects.create(
            country="Tajikistan",
            state="Sugd",
            city="Khujand",
            address="Linkoln st.21",
        )

        self.assertEqual(str(location), location.address)
