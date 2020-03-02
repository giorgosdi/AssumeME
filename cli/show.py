import click

import src.helper as helper
from src.utils import Utility
from os.path import expanduser

@click.command(name="show", help="""Shows all your temporary profiles""")
@click.option('--all', default=False, is_flag=True)
@click.pass_context
def show_command(ctx, all):
    u = Utility()
    if u.is_init():
        helper_ = helper.Helper()
        content = helper_.read_file("state")
        if content is None:
            print("You dont have a profile set in your state file. Choose a profile with `choose` command")
            exit(1)
        else:
            ## Change below line. ConfigSetup is no longer in use

            profile_config = helper_.read_file(f"{content['profile']}.prof")
            aws_profile = list(profile_config['credentials_profile'].keys())[0]
            sections=u.show_aws_profiles(profile_config, all, aws_profile)
    else:
        print("You need to initialize first")