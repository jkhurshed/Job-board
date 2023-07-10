from django.test import TestCase

from users_app.models import User

from ..models import Applicant
from contents.models import Skill


class ApplicantTest(TestCase):
    """Test model successfully created"""

    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='testpassword')

    def test_create_applicant(self):
        """Creating a category successful"""
        skill = Skill.objects.create(
            proficiency_level='junior',
        )
        applicant = Applicant.objects.create(
            name="Applicant name",
            user=self.user,
            skill=skill,
        )

        self.assertEqual(str(applicant), applicant.name)
