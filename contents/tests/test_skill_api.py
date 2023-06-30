from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from contents.models import Skill
from ..serializers import SkillSerializer

SKILL_URL = reverse("contents:skill-list")


def create_skill(user, **params):
    defaults = {
        "title": "Sample title",
        "description": "Sample description",
        "proficiency_level": "junior",
    }
    defaults.update(params)

    skill = Skill.objects.create(user=user, **defaults)
    return skill


class PublicSkillAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SKILL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSkillAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword',
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_skills(self):
        create_skill(user=self.user)

        res = self.client.get(SKILL_URL)

        skills = Skill.objects.all().order_by('id')
        serializer = SkillSerializer(skills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
