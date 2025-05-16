from typing import List
import sys
import os
from pathlib import Path

from commands_controller import command
from logs_contoller import create_log

@command(name='exit')
def exit_command(args: List[str] = None):
    """Exit from app."""

    print("Goodbye!")
    sys.exit(0)

@command(name='clear')
def clear_command(args: List[str] = None):
    """Clear all history on screen."""

    os.system('cls' if os.name == 'nt' else 'clear')

@command(name='cd')
def cd_command(args: List[str] = None):
    """Change directory/folder"""

    if not args:
       new_dir = os.path.expanduser('~')

    else:
        new_dir = args[0]

        try:
            os.chdir(new_dir)
            create_log(f"Changed dir {new_dir}", "debug")

        except Exception as e:
            print(f"Error: {e}")
            create_log(f"Error: {e}", 'error')

@command(name='mud')
def move_up_cd_command(arg: List[str] = None):
    """Move to parent directory."""

    current_dir = os.getcwd()
    parent_dir = str(Path(current_dir).parent)
        
    os.chdir(parent_dir)
    create_log(f"Move up to dir {parent_dir}", "debug")

@command(name='dir')
def dir_command(args: List[str] = None):
    """View directory files"""
    path = args[0] if args else '.'

    try:
        items = os.listdir(path)
        create_log(f"Search files in {path}", "debug")
        for item in items:
            full_path = os.path.join(path, item)
            create_log(f"Found {full_path}", "debug")
            if os.path.isdir(full_path):
                print(f"FOLDER | {item}")

            elif os.access(full_path, os.X_OK):
                print(f"FILE   | {item}")

            else:
                print(item)

    except Exception as e:
        print(f"Error: {e}")
        create_log(f"Error: {e}", 'error')
