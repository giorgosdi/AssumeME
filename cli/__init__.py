import click

from cli.generate import generate_credentials_command
from cli.choose import choose_command
from cli.clean import clean_command
from cli.configure import configure_command
from cli.export import export_command
from cli.help import help_command
from cli.initialize import initialize_command
from cli.show import show_command
from cli.whoami import whoami_command


@click.group()
@click.pass_context
def cli(ctx):
    # logging config should be configured in this function.
    pass


cli.add_command(choose_command)
cli.add_command(generate_credentials_command)
cli.add_command(choose_command)
cli.add_command(clean_command)
cli.add_command(configure_command)
cli.add_command(export_command)
cli.add_command(help_command)
cli.add_command(initialize_command)
cli.add_command(show_command)
cli.add_command(whoami_command)