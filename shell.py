# Terminode main shell

import importlib.util
import getpass
import os
import shlex
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from module_config import ModuleConfig


Command = Callable[[list[str]], bool]
ROOT = Path(__file__).parent


def load_environment() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return

    for line_number, line in enumerate(env_file.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        key, separator, value = line.partition("=")
        if not separator or not key.strip():
            print(f"Error in .env file: {line_number} line", file=sys.stderr)
            continue

        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


def get_settings() -> tuple[str, str]:
    username = os.environ.get("TERMINODE_USERNAME") or getpass.getuser()
    version = os.environ.get("TERMINODE_VERSION") or "Empty version variable"
    return username, version


def show_banner(
    username: str, version: str, modules: list[ModuleConfig]
) -> None:
    font = {
        "T": ("###", ".#.", ".#.", ".#.", ".#."),
        "E": ("###", "#..", "##.", "#..", "###"),
        "R": ("##.", "#.#", "##.", "#.#", "#.#"),
        "M": ("#.#", "###", "###", "#.#", "#.#"),
        "I": ("###", ".#.", ".#.", ".#.", "###"),
        "N": ("#.#", "###", "###", "###", "#.#"),
        "O": ("###", "#.#", "#.#", "#.#", "###"),
        "D": ("##.", "#.#", "#.#", "#.#", "##."),
    }
    for rows in zip(*(font[letter] for letter in "TERMINODE")):
        print("  " + "  ".join(rows).replace(".", " "))
    print(f"Version: {version} | User: {username}")
    print("Connected modules:")

    module_count = 1

    if modules:
        for config in modules:
            print(f"  {module_count} | {config.name} v{config.version} - {config.description}")
            module_count += 1
    else:
        print("  No modules loaded")
    print()


class CommandHandler:
    def __init__(self) -> None:
        self.commands: dict[str, Command] = {
            "help": self.help,
            "pwd": self.pwd,
            "cd": self.cd,
            "exit": self.exit,
        }

    def register(self, name: str, command: Command) -> None:
        self.commands[name] = command

    def execute(self, line: str) -> bool:
        line = line.lstrip()
        if not line:
            return True

        name = line.split(maxsplit=1)[0]
        command = self.commands.get(name)
        if command is None:
            try:
                if os.name == "nt":
                    subprocess.run(line, shell=True, check=False)
                else:
                    subprocess.run(
                        line, shell=True, executable="/bin/bash", check=False
                    )
            except OSError as error:
                print(f"Error to execute command: {error}", file=sys.stderr)
            return True

        try:
            parts = shlex.split(line, posix=os.name != "nt")
        except ValueError as error:
            print(f"Input error: {error}", file=sys.stderr)
            return True

        return command(parts[1:])

    def help(self, _args: list[str]) -> bool:
        print(f"Commands: {', '.join(sorted(self.commands))}")
        print("Other commands execute by your system.")
        return True

    @staticmethod
    def pwd(_args: list[str]) -> bool:
        print(os.getcwd())
        return True

    @staticmethod
    def cd(args: list[str]) -> bool:
        if len(args) > 1:
            print("Usage: cd [path]", file=sys.stderr)
            return True

        path = os.path.expanduser(args[0]) if args else os.path.expanduser("~")
        try:
            os.chdir(path)
        except OSError as error:
            print(f"Could not change directory: {error}", file=sys.stderr)
        return True

    @staticmethod
    def exit(_args: list[str]) -> bool:
        return False


def load_modules(handler: CommandHandler) -> list[ModuleConfig]:
    modules_dir = ROOT / "modules"
    modules_dir.mkdir(exist_ok=True)
    loaded: list[ModuleConfig] = []

    module_files = (
        path for path in modules_dir.glob("*.py") if path.name != "__init__.py"
    )
    for path in sorted(module_files):
        import_name = f"_terminode_module_{path.stem}"
        spec = importlib.util.spec_from_file_location(import_name, path)
        if spec is None or spec.loader is None:
            print(f"Error while loading module: {path}", file=sys.stderr)
            continue

        module = importlib.util.module_from_spec(spec)
        sys.modules[import_name] = module
        try:
            spec.loader.exec_module(module)
            register = getattr(module, "register", None)
            if not callable(register):
                raise AttributeError("in the module there must be a function register(handler)")
            config = getattr(module, "CONFIG", None)
            if not isinstance(config, ModuleConfig):
                raise TypeError("in the module there must be an object CONFIG of type ModuleConfig")
            register(handler)
            loaded.append(config)
        except Exception as error:
            sys.modules.pop(import_name, None)
            print(f"Error in module {path}: {error}", file=sys.stderr)

    return loaded


def run_shell() -> None:
    load_environment()
    username, version = get_settings()
    handler = CommandHandler()
    loaded_modules = load_modules(handler)
    show_banner(username, version, loaded_modules)
    prompt_char = ">" if os.name == "nt" else "$"

    while True:
        try:
            if os.path.split(os.getcwd())[-1] == "":
                line = input(f"{username} | {os.path.split(os.getcwd())[-1]} {prompt_char} ")
            else:
                line = input(f"{username} | ~/{os.path.split(os.getcwd())[-1]} {prompt_char} ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not handler.execute(line):
            break


if __name__ == "__main__":
    run_shell()
