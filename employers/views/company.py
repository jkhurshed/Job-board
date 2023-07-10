from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Company
from ..serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return self.serializer_class

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        company = self.get_object()
        serializer = self.get_serializer(company, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
