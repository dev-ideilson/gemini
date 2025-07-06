from django.urls import path, re_path
from api.core.sockets.consumer import WsConsumer

urlpatterns = [
    re_path(r'ws/core/$', WsConsumer.as_asgi(), name='core_ws')
]