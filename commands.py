from typing import List, Text
import sys
import os
from pathlib import Path
from datetime import datetime
import json

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

@command(name='fast_command', category='Terminal')
def use_fast_command_command(name: Text = None):
    """Use fast command from file. Don't use this command."""

    with open('saved_commands.json', 'r') as f:
        user_cmd = json.load(f)

    cmd = user_cmd.get(name)
    if cmd:
        return cmd
    else:
        print(f"Command not found!")
        create_log(f"Fast command not found!", 'warn')

@command(name='cfc', category='Terminal')
def create_fast_command_command(args: List[str] = None):
    """Create one-line fast command for faster input.
This command also can edit your fast commands."""
    name = input("Name of fast command (without space): ")
    fast_command = input("Command for saving: ")

    if os.path.isfile("saved_commands.json"):
        ...
    else:
        with open('saved_commands.json', 'w') as f:
            ... # Create file if not exists

    with open('saved_commands.json', 'r') as f:
        try:
            user_cmd = json.load(f)
        except json.JSONDecodeError as e:
            create_log(f"Save cmd file is empty!", 'warn')
            user_cmd = {}

    user_cmd[name] = fast_command
    with open('saved_commands.json', 'w', encoding='utf-8') as f:
        json.dump(user_cmd, f, indent=2)

    print(f'Created new fast command: {name}')
    create_log(f"Created fast command {name} with command {fast_command}", 'debug')

@command(name="dfc", category='Terminal')
def delete_fast_command_command(args: List[str] = None):
    """Delete your fast command.
Use 'dfc <fast command name>'"""
    if args == None:
        print(f"Please, enter command name in argument")
        create_log(f"Command name is None", 'error')
        return False

    if os.path.isfile("saved_commands.json"):
        ...
    else:
        with open('saved_commands.json', 'w', encoding='utf-8') as f:
            ... # Create file if not exists

    with open('saved_commands.json', 'r') as f:
        try:
            user_cmd = json.load(f)
        except json.JSONDecodeError as e:
            create_log(f"Save cmd file is empty!", 'warn')
            user_cmd = {}

    if args[0] in user_cmd:
        del user_cmd[args[0]]
    else:
        print(f"Fast command not found!")
        create_log(f"Fast command not found", 'error')
        return False
    
    with open('saved_commands.json', 'w', encoding='utf-8') as f:
        json.dump(user_cmd, f, indent=2)
    
    print(f'Command {args[0]} deleted!')
    create_log(f"Fast command {args[0]} was deleted", 'suc')

@command(name="fastcmds", category="Terminal")
def view_fast_commands_command(args: List[str] = None):
    """Print list of your fast commands"""
    if os.path.isfile("saved_commands.json"):
        ...
    else:
        with open('saved_commands.json', 'w', encoding='utf-8') as f:
            ... # Create file if not exists

    with open('saved_commands.json', 'r') as f:
        try:
            user_cmd = json.load(f)
        except json.JSONDecodeError as e:
            create_log(f"Save cmd file is empty!", 'warn')
            user_cmd = {}

    if user_cmd == {}:
        print("You dont have any fast commands!")
    else:
        max_len = max(len(cmd) for cmd in user_cmd)
        print("Your fast commands:")
        for i in user_cmd:
            print(f"{i.ljust(max_len)} | {user_cmd[i]}")