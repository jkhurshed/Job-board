"""
Tests for the CRUD applicant operations
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Applicant
from ..serializers import ApplicantSerializer, ApplicantDetailSerializer
from contents.models import Skill


APPLICANT_URL = reverse("jobs:applicant-list")


def detail_url(applicant_id):
    """Create and return a applicant detail URL."""
    return reverse('jobs:applicant-detail', args=[applicant_id])


def create_applicant(user, **params):
    """Creating default values for the applicant entity"""
    skill = Skill.objects.create(proficiency_level='junior')
    defaults = {
        "name": "Sample Name",
        "skill": skill,
    }
    defaults.update(params)

    applicant = Applicant.objects.create(user=user, **defaults)

    return applicant


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicApplicantAPITests(TestCase):
    """Test for unauthorized users"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(APPLICANT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApplicantApiTest(TestCase):
    """Tests for authorized users api requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_applicant(self):
        """Test for retrieving applicant APIs"""
        create_applicant(user=self.user)
        create_applicant(user=self.user)

        res = self.client.get(APPLICANT_URL)

        applicant = Applicant.objects.all().order_by('id')
        serializer = ApplicantSerializer(applicant, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_applicant_detail(self):
        """Test for getting applicant detail"""
        applicant = create_applicant(user=self.user)

        url = detail_url(applicant.id)
        res = self.client.get(url)

        serializer = ApplicantDetailSerializer(applicant)

        self.assertEqual(res.data, serializer.data)

    def test_create_applicant(self):
        """Test creating an applicant."""
        self.skill = Skill.objects.create(proficiency_level="junior")

        payload = {
            "name": 'Sample name',
            "skill": str(self.skill.id),
            "user": self.user.id
        }
        res = self.client.post(APPLICANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        applicant = Applicant.objects.get(id=res.data['id'])

        self.assertEqual(applicant.name, payload['name'])
        self.assertEqual(applicant.user, self.user)
        self.assertEqual(applicant.skill.proficiency_level, self.skill.proficiency_level)

    def test_partial_update(self):
        """Test for partial updating applicant"""
        self.skill = Skill.objects.create(proficiency_level="junior")

        applicant = create_applicant(user=self.user)

        payload = {
            "name": 'Sample name',
            "skill": str(self.skill.id),
            "user": self.user.id,
        }
        url = detail_url(applicant.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        applicant.refresh_from_db()

        self.assertEqual(applicant.name, payload['name'])
        self.assertEqual(applicant.user, self.user)
        self.assertEqual(applicant.skill.proficiency_level, self.skill.proficiency_level)

    def test_update_when_no_applicant_fails(self):
        new_user = create_user(email="user2@example.com", password='test123')
        applicant = create_applicant(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(applicant.id)
        self.client.put(url, payload)

        applicant.refresh_from_db()
        self.assertEqual(applicant.user, self.user)

    def test_delete_applicant(self):
        """Test deleting an applicant successful"""
        applicant = create_applicant(user=self.user)

        url = detail_url(applicant.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Applicant.objects.filter(id=applicant.id).exists())
