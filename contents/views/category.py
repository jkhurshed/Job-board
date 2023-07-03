from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Category
from ..serializers import CategorySerializer, CategoryDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return CategorySerializer

        return self.serializer_class
