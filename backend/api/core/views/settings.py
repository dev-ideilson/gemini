from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings as django_settings
from rest_framework.permissions import IsAdminUser
from api.core.models.models_app import Settings, ChatMessage, ChatSession
from api.core.serializers.core import SettingsSerializer, ChatMessageSerializer, ChatSessionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class SettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser] if not django_settings.DEBUG else [AllowAny]
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class ChatMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] if not django_settings.DEBUG else [AllowAny]
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

class ChatSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] if not django_settings.DEBUG else [AllowAny]
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

    @action(detail=True, methods=['get'], url_path='message')
    def get_messages(self, request, pk=None):
        # Detecta se o pk é numérico ou session_id
        try:
            # Primeiro tenta pegar por ID numérico
            session = ChatSession.objects.get(pk=int(pk))
        except (ValueError, ChatSession.DoesNotExist):
            # Se falhar, tenta pegar por session_id (string)
            session = get_object_or_404(ChatSession, session_id=pk)

        messages = session.messages.order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)