import subprocess
import os
import sys
from pathlib import Path

from logs_contoller import create_log


#This code will work if custom command not found
def execute_system_command(command: str):
    try:
        create_log(f"Use system command {command}", 'debug')
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )
        
        if result.stdout:
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            create_log(f"Error in sys command: {e.stderr}", 'error')

def get_script_root():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.resolve()

def find_file_in_root(filename):
    root_dir = get_script_root()
    file_path = root_dir / filename
    
    if file_path.exists():
        return file_path
    else:
        raise FileNotFoundError(f"File {filename} not found in {root_dir}")