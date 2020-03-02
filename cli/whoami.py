import click

from src.utils import Utility
from os.path import expanduser
import src.helper as helper

import yaml

APPLICATION_HOME_DIR = expanduser("~/.assume")

@click.command(name="whoami", help="""Tells you what is you current profile, based on your `state` file

Command:

assume whoami
""")
@click.pass_context
def whoami_command(ctx):
    u = Utility()
    if u.is_init():
        with open("{}/state".format(APPLICATION_HOME_DIR)) as f:
            content = yaml.load(f, Loader=yaml.FullLoader)
        if content is None:
            print("Jaqen H'ghar, is that you ?")
            print("A girl is No One")
            print("Choose a profile with aptly named command `choose` or configure one with another aplty named command `configure`")
        else:
            if content.get('profile'):
                print('Your current profile is :  {}'.format(content['profile']))
    else:
        print("You need to initialize first.")