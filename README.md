# Terminode

## Simple command-shell with module system

### Python shell

Run the shell in development mode with `python shell.py`.

### Installing the global command

To run the shell with the `terminode` command from any directory, install the
project with `pipx`. 
First install `pipx` using your system's package manager,
then run these commands from the project root:

```console
pipx ensurepath
pipx install --editable .
```

### Module system

All Python `.py` files in the `modules` directory are loaded automatically at
startup. 

To add a Python command, place a file in the `modules` directory. 

In it, define a `CONFIG` of type `ModuleConfig` with the fields `name`,
`description`, and `version`, then declare a `register(handler)` function and
register the command using `handler.register("name", function)`. 

For example, `modules/hello.py` adds the `hello [name]` command.

If a module fails, the error is printed to the terminal and the other modules continue loading.

```python
from module_config import ModuleConfig

# Configuration for module
CONFIG = ModuleConfig(
    name="Example",
    description="Example module",
    version="1.0.0",
)

# Example function
def example():
    """Example docs"""
    print(f"Example print")
    return True

# "example" - command name, example - command function
def register(handler):
    handler.register("example", example)

```