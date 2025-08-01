
from api.core.sockets.registry import HANDLER_REGISTRY

async def dispatch_message(message_type, consumer, payload):
    handler = HANDLER_REGISTRY.get(message_type)
    if handler:
        await handler(consumer, payload)
    else:
        await consumer._send_error(f"Tipo de mensagem não suportado: {message_type}")
