from typing import List, Text
import sys
import os
from pathlib import Path
from datetime import datetime

from commands_controller import command
from logs_contoller import create_log

@command(name='exit', category='Terminal')
def exit_command(args: List[str] = None):
    """Exit from app."""

    print("Goodbye!")
    sys.exit(0)

@command(name='clear', category='Terminal')
def clear_command(args: List[str] = None):
    """Clear all history on screen."""

    os.system('cls' if os.name == 'nt' else 'clear')

@command(name='cd', category='Files')
def cd_command(args: List[str] = None):
    """Change directory/folder"""

    if not args:
       new_dir = os.path.expanduser('~')

    else:
        new_dir = ''
        for i in args:
            new_dir += i
            new_dir += ' '

        try:
            os.chdir(new_dir)
            create_log(f"Changed dir {new_dir}", "debug")

        except Exception as e:
            print(f"Error: {e}")
            create_log(f"Error: {e}", 'error')

@command(name='mud', category='Files')
def move_up_cd_command(arg: List[str] = None):
    """Move to parent directory."""

    current_dir = os.getcwd()
    parent_dir = str(Path(current_dir).parent)
        
    os.chdir(parent_dir)
    create_log(f"Move up to dir {parent_dir}", "debug")

@command(name='dir', category='Files')
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

@command(name='cfl', category='Files')
def create_file_command(file_name: Text = None):
    """Create file in choosen directory with your content.
Type 'cfl <file_name>' to create file"""
    try:
        if file_name:
            checker = True
            print(f"Write your file content. Type 'end_file' to stop writing.")
            content = ''

            while checker == True:
                text = input('>>> ')
                if text != 'end_file':
                    content += f'{text}\n'
                else:
                    checker = False

            with open(file_name[0], 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"File created: {file_name[0]}")
            create_log(f"File created {file_name[0]}", 'debug')
        else:
            print(f"Choose file name!")
            create_log(f"File name was not choosen", 'warn')
    
    except Exception as e:
        print(f"Error: {e}")
        create_log(f"Error: {e}", 'error')

@command(name="dfl", category='Files')
def delete_file_command(file_name: Text = None):
    """Delete choosen file in current directory.
Type 'dfl <file name>'"""

    try:
        if os.path.isdir(file_name[0]):
            print(f"This is directory, not file!")
            create_log(f"{file_name[0]} is directory!", "warn")
            
        if not os.path.exists(file_name[0]):
            print(f"File not found: {file_name[0]}")
            create_log(f"{file_name[0]} not found!", "info")
            
        os.remove(file_name[0])
        print(f"File deleted: {file_name[0]}")
        create_log(f"{file_name[0]} deleted", "debug")

    except Exception as e:
        print(f"Error: {e}")
        create_log(f"Error: {e}", "error")


@command(name='time', category='Terminal')
def time_command(args: List[str] = None):
    """Show time now"""
    now = datetime.now()
    time_format = '%d-%m-%Y %H:%M:%S'

    print(f"Time: {now:{time_format}}")

@command(name='say', category='Terminal')
def say_command(text: Text = None):
    """Print your text on screen"""
    formatted = ''

    for i in text:
        formatted += i
        formatted += ' '

    print(formatted)