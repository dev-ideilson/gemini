from api.core.models.models_core import ModelCore
from django.db import models
from django.utils import timezone

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

class ChatSession(models.Model):
    """
    Representa uma sessão de chat única.
    Cada sessão terá seu próprio histórico de mensagens.
    """
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sessão de Chat"
        verbose_name_plural = "Sessões de Chat"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sessão {self.session_id} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class ChatMessage(models.Model):
    """
    Representa uma única mensagem dentro de uma sessão de chat.
    """
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI')])
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Mensagem de Chat"
        verbose_name_plural = "Mensagens de Chat"
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.upper()} em {self.session.session_id}: {self.text[:50]}..."


