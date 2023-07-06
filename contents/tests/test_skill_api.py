from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from contents.models import Skill
from ..serializers import SkillSerializer

SKILL_URL = reverse("contents:skill-list")


def detail_url(skill_id):
    """Create and return a recipe detail URL."""
    return reverse('contents:skill-detail', args=[skill_id])


def create_skill(**params):
    defaults = {
        "title": "Sample title",
        "description": "Sample description",
        "proficiency_level": "junior",
    }
    defaults.update(params)

    skill = Skill.objects.create(**defaults)
    return skill


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicSkillAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SKILL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSkillAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_skills(self):
        create_skill()

        res = self.client.get(SKILL_URL)

        skills = Skill.objects.all().order_by('id')
        serializer = SkillSerializer(skills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_skill_detail(self):
        skill = create_skill()

        url = detail_url(skill.id)
        res = self.client.get(url)

        serializer = SkillSerializer(skill)
        self.assertEqual(res.data, serializer.data)

    def test_create_skill(self):
        """Test creating a skill."""
        payload = {
            "title": "Sample title",
            "description": "Sample description",
            "proficiency_level": "junior",
        }
        res = self.client.post(SKILL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        skill = Skill.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(skill, k), v)

    def test_partial_update(self):
        skill = create_skill(
            title="Sample title",
            description="Sample description",
            proficiency_level="junior",
        )

        payload = {
            "title": "Sample title",
            "description": "Sample description",
            "proficiency_level": "junior",
        }
        url = detail_url(skill.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        skill.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(skill, k), v)

    def test_delete_skill(self):
        """Test deleting a skill successful"""
        skill = create_skill()

        url = detail_url(skill.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Skill.objects.filter(id=skill.id).exists())
