from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Skill
from ..serializers import SkillSerializer


class SKillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     """Create a new recipe."""
    #     serializer.save(user=self.request.user)
