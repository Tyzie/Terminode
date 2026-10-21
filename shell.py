# Terminode main shell

import importlib.util
import getpass
import os
import shlex
import shutil
import subprocess
import sys
import threading
from collections.abc import Callable
from pathlib import Path

from module_config import ModuleConfig


Command = Callable[[list[str]], bool]
PromptProvider = Callable[[], str]
InterfaceComponent = Callable[[], str]
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


def get_settings() -> tuple[str, str, float]:
    username = os.environ.get("TERMINODE_USERNAME") or getpass.getuser()
    version = os.environ.get("TERMINODE_VERSION") or "Empty version variable"
    interface_refresh_rate = float(os.environ.get("INTERFACE_REFRESHRATE")) or 1.0
    return username, version, interface_refresh_rate


def show_banner(
    username: str, version: str, modules: list[ModuleConfig]
) -> None:
    font = {
        "T": ("#########", "....#....", "....#....", "....#....", "....#...."),
        "E": ("#########", "##.......", "#######..", "##.......", "#########"),
        "R": ("######..", "##...##.", "######..", "##...##.", "##....##"),
        "M": ("##.....##", "####.####", "##.###.##", "##.....##", "##.....##"),
        "I": ("#######", "...#...", "...#...", "...#...", "#######"),
        "N": ("##....##", "####..##", "##.##.##", "##..####", "##....##"),
        "O": (".#######.", "##.....##", "##.....##", "##.....##", ".#######."),
        "D": ("######..", "##...##.", "##....##", "##...##.", "######.."),
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
            "..": self.cd_dot,
            "exit": self.exit,
            "ls": self.ls,
        }
        self.prompt_providers: list[PromptProvider] = []
        self.interface_components: list[InterfaceComponent] = []

    def register_command(self, name: str, command: Command) -> None:
        self.commands[name] = command

    def register_prompt_provider(self, provider: PromptProvider) -> None:
        self.prompt_providers.append(provider)

    def get_prompt_text(self) -> str:
        return " | ".join(
            prompt
            for provider in self.prompt_providers
            if (prompt := provider())
        )

    def register_interface_component(self, component: InterfaceComponent) -> None:
        self.interface_components.append(component)

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
        """Print available commands and their descriptions.
        Type help [command] to see more information about a command."""
        if _args != []:
            command_name = _args[0]
            command = self.commands.get(command_name)
            if command:
                if command.__doc__:
                    print(f"Additional information about command: {command_name}")
                    print(command.__doc__)
                else:
                    print(f"No available information about command: {command_name}")
            else:
                print(f"Command not found in Terminode: {command_name}")
        else:
            print(f"Commands: {', '.join(sorted(self.commands))}")
            print("Other commands execute by your system.")
            print("Type help [command] to see more information about a command.")
        return True

    @staticmethod
    def ls(args: list[str]) -> bool:
        """Print all files in current directory."""
        files = os.listdir(os.getcwd())
        print(f"Files in directory {os.path.split(os.getcwd())[-1]}: {len(files)}")
        print("")

        for file in files:
            path = Path(file)
            filetype = "Directory" if path.is_dir() else "File"
            filesize = path.stat().st_size if path.is_file() else 0

            if filesize:
                if filesize >= 1024**2:
                    filesize_text = f"{filesize / 1024**2:.2f} MB"
                elif filesize >= 1024:
                    filesize_text = f"{filesize / 1024:.2f} KB"
                else:
                    filesize_text = f"{filesize} B"
            
            else:
                filesize_text = "-"

            print(f"{filetype} | {file} {filesize_text}")

        print("")

        return True

    @staticmethod
    def pwd(_args: list[str]) -> bool:
        """Print current working directory."""
        print(os.getcwd())
        return True

    @staticmethod
    def cd(args: list[str]) -> bool:
        """Change current working directory.
        Usage only "cd" will change to the home directory."""
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
    def cd_dot(args: list[str]) -> bool:
        """Change directory to the parent directory"""
        try:
            os.chdir("..")
        except OSError as error:
            print(f"Could not change directory: {error}", file=sys.stderr)
        return True

    @staticmethod
    def exit(_args: list[str]) -> bool:
        """Exit the Terminode."""
        return False


class TerminalInterface:
    def __init__(self, components: list[InterfaceComponent], refreshrate: float) -> None:
        self.components = components
        self.refresh_interval = refreshrate
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._rendered_rows: set[int] = set()
        self._scroll_bottom: int | None = None
        self._render_lock = threading.Lock()

    def start(self) -> None:
        if not self.components or not sys.stdout.isatty():
            return

        self._stop_event.clear()
        self._render()
        self._thread = threading.Thread(target=self._refresh, daemon=True)
        self._thread.start()

    def close(self) -> None:
        if self._thread is None:
            return

        self._stop_event.set()
        self._thread.join()
        self._thread = None
        with self._render_lock:
            self._draw([])

    def _refresh(self) -> None:
        while not self._stop_event.wait(self.refresh_interval):
            self._render()

    def _render(self) -> None:
        lines: list[str] = []
        for component in tuple(self.components):
            try:
                lines.extend(component().splitlines())
            except Exception as error:
                print(f"Interface component failed: {error}", file=sys.stderr)
                self.components.remove(component)

        with self._render_lock:
            self._draw(lines)

    def _draw(self, lines: list[str]) -> None:
        columns, terminal_rows = shutil.get_terminal_size(fallback=(80, 24))
        visible_lines = lines[-max(terminal_rows - 1, 1) :]
        first_row = terminal_rows - len(visible_lines) + 1
        scroll_bottom = max(first_row - 1, 1)
        current_rows = set(range(first_row, terminal_rows + 1))
        output = ["\x1b[s"]
        if scroll_bottom != self._scroll_bottom:
            output.extend((f"\x1b[1;{scroll_bottom}r", "\x1b[u", "\x1b[s"))
            self._scroll_bottom = scroll_bottom
        for offset, line in enumerate(visible_lines):
            output.extend(
                (f"\x1b[{first_row + offset};1H", "\x1b[2K", line[:columns])
            )
        for row in sorted(self._rendered_rows - current_rows):
            output.extend((f"\x1b[{row};1H", "\x1b[2K"))
        output.append("\x1b[u")
        sys.stdout.write("".join(output))
        sys.stdout.flush()
        self._rendered_rows = current_rows


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
    username, version, refreshrate = get_settings()
    handler = CommandHandler()
    loaded_modules = load_modules(handler)
    terminal_interface = TerminalInterface(handler.interface_components, refreshrate)
    terminal_interface.start()

    try:
        show_banner(username, version, loaded_modules)
        prompt_char = ">" if os.name == "nt" else "$"

        while True:
            try:
                additional_prompt = handler.get_prompt_text()
                additional_prompt_text = f" | {additional_prompt}" if additional_prompt else ""
                if os.path.split(os.getcwd())[-1] == "":
                    prompt = input(
                        f"{username}{additional_prompt_text} | {os.path.split(os.getcwd())[-1]} "
                        f"{prompt_char} "
                    )
                else:
                    prompt = input(
                        f"{username}{additional_prompt_text} | ~/{os.path.split(os.getcwd())[-1]} "
                        f"{prompt_char} "
                    )
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not handler.execute(prompt):
                break
    finally:
        terminal_interface.close()


if __name__ == "__main__":
    run_shell()
