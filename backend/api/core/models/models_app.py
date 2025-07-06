from api.core.models.models_core import ModelCore
from django.db import models


class Settings(models.Model):
    """
    Model to store application settings.
    """
    key = models.CharField(max_length=255, unique=True, db_index=True)
    value = models.TextField(default='', blank=True, null=True)

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
    
    def get_value(self, key: str, default:str=None) -> any:
        """
        Returns the value of the setting.
        """
        try:
            setting = Settings.objects.get(key=key)
            return setting.value
        except Settings.DoesNotExist:
            return default
    
    def set_value(self, key: str, value: any) -> None:
        """
        Sets the value of the setting.
        If the setting does not exist, it creates a new one.
        """
        setting, created = Settings.objects.get_or_create(key=key)
        setting.value = value
        setting.save()
