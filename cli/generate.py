import click

from src.utils import Utility
import src.helper as helper
from src.section import Section


@click.command(name="generate", help="Creates temporary credentials out of the current profile")
@click.pass_context
def generate_credentials_command(ctx):
    u = Utility()
    if u.is_init():
        helper_ = helper.Helper()
        content = helper_.read_file("state")
        creds = u.get_credentials(content['user'])
        profile_config = helper_.read_file("{}.prof".format(content['profile']))

        Section.create_section(
            profile_config,
            content['user'],
            creds
        )
    else:
        print("You need to initialize first.")