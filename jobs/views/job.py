from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Job
from ..serializers import JobDetailSerializer, JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobDetailSerializer
    queryset = Job.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return JobSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
