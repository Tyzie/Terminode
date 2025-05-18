import os
from typing import List
from datetime import datetime

import config
from sys_controller import execute_system_command
import commands #This import need for loading built-in module
from commands_controller import commands_return, load_modules
from logs_contoller import create_log


#This controller will load user custom modules
load_modules('modules')
now = datetime.now()
time_format = '%H:%M:%S'

if os.name == 'nt':
    os.system('chcp 65001 > nul')

class Terminode:
    def __init__(self):
        self.version = config.console_version
        self.cur_dir = os.getcwd()
        self.username = config.username
        self.prompt = f"{now:{time_format}} | {self.username} | {self.cur_dir} | "
        self.commands = commands_return()

    def parse_input(self, input_str: str) -> List[str]:
        return input_str.strip().split()

    def run(self):
        print(f"Terminode - {self.version}")
        print("Enter 'help' for commands list / Enter 'exit' for exit app")
        create_log('Started Terminode', 'info')
        
        while True:
            try:
                user_input = input(self.prompt).strip()
                if not user_input:
                    continue
                
                parts = self.parse_input(user_input)
                command_name = parts[0]
                args = parts[1:] if len(parts) > 1 else None
                
                if command_name in self.commands:
                    self.commands[command_name](args)
                else:
                    execute_system_command(user_input)
                self.update_prompt()
                    
            except KeyboardInterrupt:
                print("\nFor quit enter 'exit'")
                create_log("Type exit for quit", "warning")

            except EOFError:
                print()
                self.exit_command()

            except Exception as e:
                print(f"Error: {e}")
                create_log(f"Error: {e}", "error")

    def update_prompt(self):
        self.prompt = f"{now:{time_format}} | {self.username} | {os.getcwd()} | "

terminal = Terminode()
terminal.run()