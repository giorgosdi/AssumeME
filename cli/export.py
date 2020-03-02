import click

from src.utils import Utility
import src.helper as helper

@click.command(name="export", help="Print the command to export the AWS profile")
@click.pass_context
def export_command(ctx):
    u = Utility()
    if u.is_init():
        helper_ = helper.Helper()
        content = helper_.read_file("state")
        profile_config = helper_.read_file(f"{content['profile']}.prof")
        aws_profile = list(profile_config['credentials_profile'].keys())
        
        if content is None:
            print("You dont have a profile set in your state file. Choose a profile with `choose` command")
            exit(1)
        else:
            print(f"export AWS_PROFILE={aws_profile[0]}")
    else:
        print("You need to initialize first")