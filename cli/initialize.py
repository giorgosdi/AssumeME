import click

from src.utils import Utility
import src.helper as helper
from os.path import expanduser

import os

APPLICATION_HOME_DIR = expanduser("~/.assume")

@click.command(name="init", help="Initialize asm")
@click.pass_context
def initialize_command(ctx):
    u = Utility()
    if os.path.isdir(APPLICATION_HOME_DIR):
        directory = True
        if os.path.exists(f"{APPLICATION_HOME_DIR}/state"):
            state = True
        else:
            state = False
    else:
        directory = False
    
    if directory and state:
        print("Good news, `asm` is already initialized !")

    if not directory:
        u.create_directory(APPLICATION_HOME_DIR)
        u.create_file(APPLICATION_HOME_DIR, "state")
        state = True
        print("Initialization was successful..")
    if not state:
        u.create_file("state")