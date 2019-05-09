import click
from src.configure import ConfigureAwsAssumeRole
from src.utils import Utility
from os.path import expanduser
import os
import subprocess
import yaml
import src.helper as helper

class ConfigSetup(click.Group):
    def __init__(self, profile):
        u = Utility()
        self.profile = profile
        self.profile_config = u.read_configuration(self.profile)
        self.application_home_dir = expanduser("~/.assume")
        self.aws_creds_path=expanduser(self.profile_config['credentials'])
        self.aws_config_path=expanduser(self.profile_config['config'])
        self.aws_creds, self.aws_config = u.create_config_parsers([self.aws_creds_path, self.aws_config_path])

APPLICATION_HOME_DIR = expanduser("~/.assume")

@click.group()
@click.pass_context
def actions(ctx):
    if os.path.isfile("{}/state".format(APPLICATION_HOME_DIR)):
        with open("{}/state".format(APPLICATION_HOME_DIR)) as f:
            content=yaml.load(f, Loader=yaml.FullLoader)
        
        if content is not None:
            if content.get('profile'):
                ctx.obj = ConfigSetup(content['profile'])
    else:
        print("State file does not exists.")
        aux = helper.Helper()
        profiles = aux.get_profiles()
        if profiles:
            profile=input('Choose one of these profiles : ')
            while profile not in profiles:
                profile=input('This profile does not exist. Choose a profile from the list above : ')
            aux.write_state_file({'profile': profile})
            ctx.obj = ConfigSetup(profile)
        else:
            print("There are no profiles available, you should create a new profile.")
            configure()
                


@actions.command(help="Choose a profile and add it in your state file")
@click.argument('profile')
@click.pass_context
def choose(ctx, profile):
    helper_ = helper.Helper()
    profiles = helper_.get_profiles()
    if profile in profiles:
        helper_.write_state_file({'profile': profile})
        ctx.obj = ConfigSetup(profile)
    else:
        print("The profile does not exist")
        if profiles:
            print("Pick one of the")
            for p in profiles:
                print("- {}".format(p))
        else:
            print("There are no profiles. Configure a profile please")


@actions.command(help="""Tells you what is you current profile, based on your `state` file

Command:

assume whoami
""")
@click.pass_context
def whoami(ctx):
    with open("{}/state".format(APPLICATION_HOME_DIR)) as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
    if content is None:
        print("Jaqen H'ghar, is that you ?")
        print("A girl is No One")
        print("Choose a profile with aptly named command `choose` or configure one with another aplty named command `configure`")
    else:
        if content.get('profile'):
            print('Your current profile is :  {}'.format(content['profile']))




@actions.command(help="""Creates temporary credentials out of the current profile

Command:

assume generate
""")
# @click.argument('profile')  # add the name argument
@click.pass_context
def generate(ctx):
    u = Utility()
    creds = u.get_credentials(ctx.obj.profile_config['credentials_profile'])
    aws_creds, aws_config = u.create_config_parsers([ctx.obj.aws_creds_path, ctx.obj.aws_config_path])
    u.create_section(
        aws_creds,
        aws_config,
        ctx.obj.profile_config['credentials_profile'],
        creds,
        ctx.obj.aws_creds_path,
        ctx.obj.aws_config_path
    )


@actions.command(help="""Shows all your temporary profiles""")
@click.option('--all', default=False, is_flag=True)
@click.pass_context
def show(ctx, all):
    if ctx.obj is None:
        print("A girl is No One. Pick a user with `choose` or configure one with `configure`")
        exit(1)
    else:
        u = Utility()
        sections=u.discover_sections(ctx.obj.aws_creds, all, ctx.obj.profile)

@actions.command(help="Deletes all profiles that passed the expiration date and asks you if you want to delete the valid ones")
@click.pass_context
def clean(ctx):
    if ctx.obj is not None:
        if os.path.isfile("{}/state".format(APPLICATION_HOME_DIR)):
            with open("{}/state".format(APPLICATION_HOME_DIR)) as f:
                content=yaml.load(f, Loader=yaml.FullLoader)
            
            if content is not None:
                if content.get('profile'):
                    profile = ConfigSetup(content['profile'])


@actions.command(help="Configure a new profile with your prefered settings.")
def configure():
    u = Utility()

    u.print_message('Provide your configuration - leave blank for defaults in brackets')
    name = input("Configuration name [MyNewConfig] : ") or "MyNewConfig"
    config_path = input('AWS config path [~/.aws/config] : ') or '~/.aws/config'
    credentials_path = input('AWS credentials path [~/.aws/credentials] : ') or '~/.aws/credentials'
    token_duration = input('Duration of profile in seconds [86400 - one day] : ') or '86400'
    region = input('Region [eu-west-1] : ') or 'eu-west-1'
    output = input('Output [text] : ') or 'text'
    profile = input('Profile to associate this configuration [default] : ') or 'default'

    conf = ConfigureAwsAssumeRole(
        config_path=config_path,
        credentials_path=credentials_path,
        configuration_name=name,
        token_duration=token_duration,
        region=region,
        output=output,
        credentials_profile=profile
    )
    conf.create_config(conf.config)

@actions.command(help="You are using it right now")
@click.pass_context
def help(ctx):
    print(actions.get_help(ctx))

def main():
    actions()
# if __name__ == '__main__':
#     actions()