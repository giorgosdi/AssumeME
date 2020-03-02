import click

@click.command(name="help", help="You are using it right now")
@click.pass_context
def help_command(ctx):
    print(click.get_help(ctx))
