"""
View for token authentication api.
"""
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users_app.serializers import AuthTokenSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
