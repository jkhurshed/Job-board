from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Location
from ..serializers import LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
