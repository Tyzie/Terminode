# CPU and RAM load in interface and prompt

import os

from module_config import ModuleConfig


CONFIG = ModuleConfig(
    name="Interface and prompt resources example",
    description="Show CPU load and RAM usage at the bottom of the terminal and in prompt line",
    version="1.0.0"
)


def get_status() -> str:
    """Return available CPU load and RAM metrics."""
    metrics = []

    getloadavg = getattr(os, "getloadavg", None)
    if getloadavg is not None:
        try:
            metrics.append(f"CPU load (1m): {getloadavg()[0]:.2f}")
        except OSError:
            metrics.append("CPU load: unavailable")
    else:
        metrics.append("CPU load: unavailable")

    sysconf = getattr(os, "sysconf", None)
    try:
        total_pages = sysconf("SC_PHYS_PAGES") if sysconf else 0
        available_pages = sysconf("SC_AVPHYS_PAGES") if sysconf else 0
        if total_pages > 0:
            used_percent = 100 * (1 - available_pages / total_pages)
            metrics.append(f"RAM: {used_percent:.0f}%")
        else:
            metrics.append("RAM: unavailable")
    except (OSError, ValueError):
        metrics.append("RAM: unavailable")

    return " | ".join(metrics)

def prompt_status() -> str:
    """Return available CPU load in prompt line."""
    cpu = ""

    getloadavg = getattr(os, "getloadavg", None)
    if getloadavg is not None:
        try:
            cpu = f"CPU load: {getloadavg()[0]:.2f}"
        except OSError:
            cpu = "CPU load: unavailable"
    else:
        cpu = "CPU load: unavailable"

    return cpu

def register(handler) -> None:
    handler.register_prompt_provider(prompt_status)
    handler.register_interface_component(get_status)
