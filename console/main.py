import os
from typing import List

import config
from sys_controller import execute_system_command
import commands #This import need for loading built-in module
from commands_controller import commands_return, load_modules


#This controller will load user custom modules
load_modules('modules')

class Terminode:
    def __init__(self):
        self.version = config.console_version
        self.cur_dir = os.getcwd()
        self.username = config.username
        self.input_line = f"{self.username} | {self.cur_dir} | "
        self.commands = commands_return()

    def parse_input(self, input_str: str) -> List[str]:
        return input_str.strip().split()

    def run(self):
        print(f"Terminode - {self.version}")
        print("Enter 'help' for commands list / Enter 'exit' for exit app")
        
        while True:
            try:
                user_input = input(self.input_line).strip()
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

            except EOFError:
                print()
                self.exit_command()

            except Exception as e:
                print(f"Error: {e}")

    def update_prompt(self):
        self.input_line = f"{self.username} | {os.getcwd()} | "

terminal = Terminode()

terminal.run()