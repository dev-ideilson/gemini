import importlib
from pathlib import Path

def auto_register_handlers():
    """
    Automatically registers all handlers in the current directory.
    """
    handlers_dir = Path(__file__).parent
    for path in handlers_dir.glob("*.py"):
        if path.name != "__init__.py":
            importlib.import_module(f"api.core.handlers.{path.stem}")