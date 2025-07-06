HANDLER_REGISTRY = {}

def register_handler(message_type):
    def decorator(func):
        HANDLER_REGISTRY[message_type] = func
        return func
    return decorator
