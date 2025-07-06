import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from api.core.sockets.dispatch import dispatch_message

class WsConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for core functionalities.
    Handles incoming messages and sends responses.
    """

    async def connect(self):
        self.user = self.scope.get('user', None)
        self.channel_group_name = self.get_channel_group_name()
        
        if not self.user or not getattr(self.user, 'is_authenticated', False):
            return await self.close(code=4000)
        
        if not await self.has_permission():
            return await self.close(code=4001)
        
        await self.channel_layer.group_add(
            self.channel_group_name,
            self.channel_name
        )
       
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.channel_group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        message_type = content.get("type")
        payload = content.get("payload", {})
        await dispatch_message(message_type, self, None, payload)
    
    def get_channel_group_name(self):
        """
        Returns the channel group name for this consumer.
        """
        return f"user_{self.user.id}_group" if self.user else 'plublic_group'


    async def has_permission(self) -> bool:
        return True  # sobrescrito nos filhos