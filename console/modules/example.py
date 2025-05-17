from typing import List
#Commands controller will load your commands
from commands_controller import command, module

module('Simple Example Module')

#Example command
@command(name='example_command', category='Module')
def test_command(args: List[str] = None):
    # This desc will show in help command
    """Its a description of this command."""
    print('Its example command. You can replace this code to your code.')