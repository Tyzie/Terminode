from typing import List, Dict, Callable, Optional
from functools import wraps
from pathlib import Path
import importlib
import inspect

import config

COMMANDS: Dict[str, Callable] = {}
MODULES: Dict[str, Callable] = {}

def command(name: Optional[str] = None):
    def decorator(func):
        cmd_name = name or func.__name__
        register_command(cmd_name, func)
            
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def module(name: Optional[str] = None):
    MODULES[name] = name

def register_command(name: str, func: Callable):
    COMMANDS[name] = func

def load_modules(folder_path: str):
    folder = Path(folder_path)
    
    for file in folder.glob("*.py"):
        module_name = file.stem
        
        if module_name.startswith("_"):
            continue
        
        try:
            module = importlib.import_module(f"{folder_path}.{module_name}")
            
            for _, func in inspect.getmembers(module, inspect.isfunction):
                if hasattr(func, "_is_command"):
                    cmd_name = getattr(func, "_command_name", func.__name__)
                    COMMANDS[cmd_name] = func
                    
        except ImportError as e:
            print(f"Loading error {module_name}: {e}")

@command(name='help')
def help_command(args: List[str] = None):
    """Print list of commands"""

    print(f"Command list:")
    max_len = max(len(cmd) for cmd in COMMANDS)

    for cmd, func in sorted(COMMANDS.items()):
        doc = func.__doc__ or "Description not found"
        print(f" {cmd.ljust(max_len)} - {doc}")

def commands_return():
    if MODULES:
        for i in MODULES:
            module_check = f'Modules - {config.modules_version}\nLoaded modules:\n'
            module_check += f'{i}\n'
            
        print(module_check)

    return COMMANDS