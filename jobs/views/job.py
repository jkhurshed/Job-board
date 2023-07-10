from rest_framework.authentication import TokenAuthentication
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ..models import Job
from ..serializers import JobDetailSerializer, JobSerializer
from ..filters import JobFilter


class JobViewSet(GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin
                 ):
    serializer_class = JobDetailSerializer
    queryset = Job.objects.all()
    http_method_names = ['get', 'patch', 'post', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = JobFilter

    def get_queryset(self):
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(jobs__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('title').distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return JobSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
