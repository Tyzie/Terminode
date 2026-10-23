"""Show CPU and RAM usage in the interface and prompt."""

import sys
import threading
from pathlib import Path
from typing import Optional

try:
    import psutil
except ModuleNotFoundError as error:
    if error.name != "psutil":
        raise
    psutil = None

from module_config import ModuleConfig


CONFIG = ModuleConfig(
    name="Interface and prompt resources example",
    description="Show CPU load and RAM usage at the bottom of the terminal and in prompt line",
    version="1.0.0",
)

_cpu_lock = threading.Lock()
_previous_cpu_times: Optional[tuple[int, int]] = None


def _linux_cpu_percent() -> float:
    global _previous_cpu_times

    cpu_fields = Path("/proc/stat").read_text(encoding="ascii").splitlines()[0].split()
    if not cpu_fields or cpu_fields[0] != "cpu":
        raise RuntimeError("Could not read aggregate CPU counters from /proc/stat")

    counters = [int(value) for value in cpu_fields[1:]]
    total = sum(counters)
    idle = counters[3] + (counters[4] if len(counters) > 4 else 0)

    with _cpu_lock:
        previous = _previous_cpu_times
        _previous_cpu_times = (total, idle)

    if previous is None:
        return 0.0

    total_delta = total - previous[0]
    idle_delta = idle - previous[1]
    if total_delta <= 0:
        return 0.0
    return max(0.0, min(100.0, 100 * (total_delta - idle_delta) / total_delta))


def _linux_memory_percent() -> float:
    memory: dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
        key, separator, value = line.partition(":")
        if separator:
            memory[key] = int(value.strip().split()[0])

    total = memory.get("MemTotal")
    available = memory.get("MemAvailable")
    if total is None or available is None or total <= 0:
        raise RuntimeError("Could not read memory totals from /proc/meminfo")
    return max(0.0, min(100.0, 100 * (total - available) / total))


def _cpu_percent() -> float:
    if psutil is not None:
        return psutil.cpu_percent(interval=None)
    if sys.platform.startswith("linux"):
        return _linux_cpu_percent()
    raise RuntimeError("Install the project dependencies to enable CPU metrics")


def _memory_percent() -> float:
    if psutil is not None:
        return psutil.virtual_memory().percent
    if sys.platform.startswith("linux"):
        return _linux_memory_percent()
    raise RuntimeError("Install the project dependencies to enable RAM metrics")


def get_status() -> str:
    """Return available CPU load and RAM metrics."""
    cpu_percent = _cpu_percent()
    memory_percent = _memory_percent()
    return f"CPU: {cpu_percent:.0f}% | RAM: {memory_percent:.0f}%"


def prompt_status() -> str:
    """Return current CPU usage in the prompt line."""
    return f"CPU: {_cpu_percent():.0f}%"


def register(handler) -> None:
    handler.register_prompt_provider(prompt_status)
    handler.register_interface_component(get_status)
