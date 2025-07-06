from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings as django_settings
from rest_framework.permissions import IsAdminUser
from api.core.models.models_app import Settings
from api.core.serializers.core import SettingsSerializer

class SettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser] if not django_settings.DEBUG else [AllowAny]
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer