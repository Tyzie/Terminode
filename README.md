# Terminode

[![wakatime](https://wakatime.com/badge/user/8cd3262f-0285-4bdc-9986-ca6d4ed03976/project/9be3619a-cf12-44e4-a156-d4f4a376da79.svg)](https://wakatime.com/badge/user/8cd3262f-0285-4bdc-9986-ca6d4ed03976/project/9be3619a-cf12-44e4-a156-d4f4a376da79)

## Terminode - console app, that can make work some faster.
Terminode is console app. But in future it will get an terminal emulator.
Our app is open-source, and everyone can edit it.

For work need Python 3.x

## Start working with Terminode
### Installing
#### 1. Clone repository
``` bash
git clone https://github.com/Tyzie/Terminode
```
#### 2. Go to folder `console`

After this there are two ways to start app.

1. Find file `start.bat` and run it. Terminode will start up automatically.

2. Find file `main.py`. Run console and write:
```python
python main.py
```
After this Terminode will load in your terminal.

### Working with commands
Now Terminode have small list of commands.
If you want to view this list - write 'help' in Terminode.

### Changing settings
The settings of Terminode are located in the file `config.py`.
In config you can change your username.
Also you can to turn off logs (logs default on)

To change the name, enter new data into the variable `username`

Example: `username = 'terminode'`

### Writing custom modules
#### Main information about modules
In folder `modules` users can make custom modules for Terminode (mods).
In this folder you can see two files:
1. example.py
2. for_devs.md

In markdown file you can see some information about writing mods for Terminode. In python file you can see some example code for modules.

#### Connect modules
To connect a custom module, import the module `module` from `commands_controller`.

Then write `module('Name of your module')`

Commands controller will automatically load your module into Terminode!

##### This README file will changed with updates!