# Example of custom modules and commands for Terminode

from module_config import ModuleConfig


CONFIG = ModuleConfig(
    name="Hello, example!",
    description="Example simple module for Terminode",
    version="1.0.0",
)


def hello(args):
    """Print an example hello message"""
    name = " ".join(args) or "user"
    print(f"Hello, {name}!")
    return True


def register(handler):
    handler.register("hello", hello)
