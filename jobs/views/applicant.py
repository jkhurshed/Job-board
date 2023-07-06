from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Applicant
from ..serializers import ApplicantSerializer, ApplicantDetailSerializer


class ApplicantViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicantDetailSerializer
    queryset = Applicant.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicantSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
