import click

import src.helper as helper_
from src.utils import Utility
from os.path import expanduser

@click.command(name="clean", help="Deletes all profiles that passed the expiration date and asks you if you want to delete the valid ones")
@click.pass_context
def clean_command(ctx):
    u = Utility()
    if u.is_init():
        helper_ = helper.Helper()
        content = helper_.read_file("state")
        if content is None:
            print("You dont have a profile set in your state file. Choose a profile with `choose` command")
            exit(1)
        else:
            if content.get("profile"):
                profile_config = helper_.read_file(content["profile"])
                parsers = {
                    "config": profile_config["config"],
                    "credentials": profile_config["credentials"]
                }
                paths = {
                    "config": expanduser(profile_config["config"]),
                    "credentials": expanduser(profile_config["credentials"])
                }
                u.clean_sections(parsers, paths)