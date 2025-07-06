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
    
    @classmethod
    def get_value(cls, key: str, default: str = None):
        try:
            setting = cls.objects.get(key=key)
            return setting.value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_value(cls, key: str, value) -> None:
        setting, created = cls.objects.get_or_create(key=key)
        setting.value = value
        setting.save()
