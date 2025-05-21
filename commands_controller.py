from typing import List, Dict, Callable, Optional
from functools import wraps
from pathlib import Path
import importlib
import inspect

import config
from logs_contoller import create_log
from sys_controller import (find_file_in_root,
                            get_script_root)

COMMANDS: Dict[str, Callable] = {}
MODULES: Dict[str, Callable] = {}
CATEGORIES: Dict[str, Callable] = {}

def command(name: Optional[str] = None, category: Optional[str] = None):
    def decorator(func):
        cmd_name = name or func.__name__
        cmd_category = category
        register_command(cmd_name, cmd_category, func)
            
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def module(name: Optional[str] = None):
    MODULES[name] = name
    create_log(f"Registered module: {name}", "info")

def register_command(name: str, category: str, func: Callable):
    COMMANDS[name] = func
    if category == None:
        category = 'Unknown'
    CATEGORIES[name] = category
    create_log(f"Registered command: {name} with category {category}", "info")

def load_modules(folder_path: str):
    sc_folder = Path(get_script_root())
    folder = Path(sc_folder / folder_path)
    
    for file in folder.glob("*.py"):
        module_name = file.stem
        
        if module_name.startswith("_"):
            continue
        
        try:
            module = importlib.import_module(f"{folder_path}.{module_name}")
            create_log(f"Found module {module}", "debug")
            for _, func in inspect.getmembers(module, inspect.isfunction):
                if hasattr(func, "_is_command"):
                    cmd_name = getattr(func, "_command_name", func.__name__)
                    cmd_ctgr = getattr(func, "_command_category")
                    register_command(cmd_name, cmd_ctgr, func)
                    
        except ImportError as e:
            print(f"Loading error {module_name}: {e}")
            create_log(f"Error load module {module_name}: {e}", "error")

@command(name='help', category='Terminal')
def help_command(args: List[str] = None):
    """Print list of commands.
Type 'help <category>' to see commands in choosen category."""

    if args == None:
        print(f"Command list:")
        max_len = max(len(cmd) for cmd in COMMANDS)
        max_key = max(CATEGORIES.keys(), key=lambda k: len(CATEGORIES[k]))
        max_value = len(CATEGORIES[max_key])
    
        for cmd, func in sorted(COMMANDS.items()):
            doc = func.__doc__ or "Description not found"
            categ = str(CATEGORIES.get(cmd))
            print(f"{categ.ljust(max_value)} > {cmd.ljust(max_len)}\n{doc}\n")

    else:
        print(f"Command list on category {args[0]}:")
        max_len = max(len(cmd) for cmd in COMMANDS)
        max_key = max(CATEGORIES.keys(), key=lambda k: len(CATEGORIES[k]))
        max_value = len(CATEGORIES[max_key])
    
        for cmd, func in sorted(COMMANDS.items()):
            doc = func.__doc__ or "Description not found"
            categ = str(CATEGORIES.get(cmd))
            if categ.lower() == args[0].lower():
                print(f"{categ.ljust(max_value)} > {cmd.ljust(max_len)}\n{doc}\n")

@command(name='ctgs', category='Terminal')
def categories_help_command(args: List[str] = None):
    """Print list of categories"""
    print('All categories:')
    max_key = max(CATEGORIES.keys(), key=lambda k: len(CATEGORIES[k]))
    max_value = len(CATEGORIES[max_key])

    for cat in set(CATEGORIES.values()):
        print(f'| {cat.ljust(max_value)} |')

def commands_return():
    if MODULES:
        for i in MODULES:
            module_check = f'Modules - {config.modules_version}\nLoaded modules:\n'
            module_check += f'{i}\n'
            
        print(module_check)

    return COMMANDS