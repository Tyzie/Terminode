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
`description`, and `version`

Commands can register with `handler.register_command("name", function)`

Customize the interface with `handler.register_interface_component(function)`.
An interface component returns text to display at the bottom of the terminal;

Prompt status providers can also be registered with
`handler.register_prompt_provider(function)`;
they return a short string displayed beside the prompt.

Examples:

- `modules/hello.py` adds the `hello [name]` command.
- `modules/editor.py` adds `edit <file>`, which launches the editor in `$EDITOR`
  (or `vi`/`notepad` by default).
- `modules/system_status.py` adds `resources` and displays CPU load and RAM
  usage at the bottom of the terminal and in prompt line. On Linux, it reads
  metrics from `/proc` when `psutil` is not installed.

If a module fails, the error is printed to the terminal and the other modules continue loading.