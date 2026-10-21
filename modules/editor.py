# Open files in system text editors

import os
import shlex
import subprocess
import sys
from pathlib import Path

from module_config import ModuleConfig


CONFIG = ModuleConfig(
    name="Text editor example",
    description="Open files in the editor configured by the system",
    version="1.0.0"
)


def edit(args: list[str]) -> bool:
    """Open a file in $EDITOR (or notepad/vi by default). Usage: edit <file>."""
    if len(args) != 1:
        print("Usage: edit <file>", file=sys.stderr)
        return True

    editor = os.environ.get("EDITOR") or ("notepad" if os.name == "nt" else "vi")
    try:
        editor_command = shlex.split(editor, posix=os.name != "nt")
    except ValueError as error:
        print(f"Invalid EDITOR setting: {error}", file=sys.stderr)
        return True

    if not editor_command:
        print("EDITOR is empty; set it to an editor command.", file=sys.stderr)
        return True

    try:
        subprocess.run([*editor_command, str(Path(args[0]).expanduser())], check=False)
    except OSError as error:
        print(f"Could not start editor: {error}", file=sys.stderr)
    return True


def register(handler) -> None:
    handler.register_command("edit", edit)
