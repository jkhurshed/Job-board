"""
Testing test entity
"""
from django.test import TestCase

from users_app.models import User

from ..models import Skill


class SkillTest(TestCase):
    """Test model"""

    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='testpassword')

    # name, description, proficiency level,
    def test_create_skill(self):
        """Creating a category successful"""
        skill = Skill.objects.create(
            title="Sample category title",
            description="Sample description",
        )

        self.assertEqual(str(skill), skill.proficiency_level)

    def test_proficiency_level_choices(self):
        # Retrieve the choices from the model field
        choices = Skill._meta.get_field('proficiency_level').choices

        # Extract the values from the choices
        values = [choice[0] for choice in choices]

        # Define the expected values
        expected_values = ['junior', 'middle', 'senior', 'team lead']

        # Assert that the values match the expected values
        self.assertEqual(values, expected_values)
