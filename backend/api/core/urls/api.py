# apps/urls/v3.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.core.views import auth 
from api.core.views.settings import SettingsViewSet
from api.core.views.settings import SettingsViewSet

router = DefaultRouter()
router.register(r'users', auth.UsersViewSet, basename='users')
router.register(r'settings', SettingsViewSet, basename='settings')
# router.register(r'ai/chats', AiChatViewSet, basename='ai-chats')
# router.register(r'ai/prompts', AiPromptViewSet, basename='ai-prompts')
# router.register(r'ai/errors', AiErrorViewSet, basename='ai-errors')


urlpatterns = [
    path('auth/login/', auth.LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', auth.RefreshTokenView.as_view(), name='auth-refresh'),
    path('auth/me/', auth.UserMeView.as_view(), name='auth-me'),
    # path('auth/register/', auth.RegisterView.as_view(), name='auth-register'),
    path('', include(router.urls)),
]
