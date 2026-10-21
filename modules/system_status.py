# CPU and RAM load in interface and prompt

import psutil

from module_config import ModuleConfig


CONFIG = ModuleConfig(
    name="Interface and prompt resources example",
    description="Show CPU load and RAM usage at the bottom of the terminal and in prompt line",
    version="1.0.0"
)


def get_status() -> str:
    """Return available CPU load and RAM metrics."""
    cpu_percent = psutil.cpu_percent(interval=None)
    memory_percent = psutil.virtual_memory().percent
    return f"CPU: {cpu_percent:.0f}% | RAM: {memory_percent:.0f}%"

def prompt_status() -> str:
    """Return current CPU usage in the prompt line."""
    return f"CPU: {psutil.cpu_percent(interval=None):.0f}%"

def register(handler) -> None:
    handler.register_prompt_provider(prompt_status)
    handler.register_interface_component(get_status)
