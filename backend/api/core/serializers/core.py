from rest_framework import serializers
from api.core.models.models_app import Settings

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'