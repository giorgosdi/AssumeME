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
        helper_ = helper.Helper()
        self.profile = profile
        self.profile_config = u.read_configuration(self.profile)
        self.current_state = helper_.read_file('state')
        self.application_home_dir = expanduser("~/.assume")
        self.aws_creds_path=expanduser(self.profile_config['credentials'])
        self.aws_config_path=expanduser(self.profile_config['config'])
        self.aws_creds, self.aws_config = u.create_config_parsers([self.aws_creds_path, self.aws_config_path])

APPLICATION_HOME_DIR = expanduser("~/.assume")

@click.group()
@click.pass_context
def actions(ctx):
    helper_ = helper.Helper()
    if os.path.isfile("{}/state".format(APPLICATION_HOME_DIR)):
        content = helper_.read_file('state')
        if content is not None:
            if content.get('profile'):
                ctx.obj = ConfigSetup(content['profile'])
    else:
        print("State file does not exists.")
        profiles = helper_.get_profiles()
        if profiles:
            profile=input('Choose one of these profiles : ')
            while profile not in profiles:
                profile=input('This profile does not exist. Choose a profile from the list above : ')
            content = helper_.read_file('{}.prof'.format(profile))
            profile_ = content['profile']
            user_ = list(content['credentials_profile'].keys())[0]
            role_ = list(content['credentials_profile'][user_].keys())[0]
            account_ = content['credentials_profile'][user_][role_]
            helper_.write_file('state', {
                    'profile': profile_,
                    'user': user_,
                    'role': role_,
                    'account': account_
                })
            ctx.obj = ConfigSetup(profile)
        else:
            print("There are no profiles available, you should create a new profile.")
            config()
                


@actions.command(help="Choose a profile and add it in your state file")
@click.argument('profile')
@click.option('--role')
@click.option('--user')
@click.pass_context
def choose(ctx, profile, user, role):
    helper_ = helper.Helper()
    details = helper_.read_file("{}.prof".format(profile))
    users = list(details['credentials_profile'].keys())
    
    if not user:
        print("You have these users:")
        for u in users:
            print('- {}'.format(u))
        user = input("Pick a role : ")

    while user not in users:
        user = input("The user you chose does not exist.. Pick a valid user")
    
    roles = list(details['credentials_profile'][user].keys())
    if not role:
        print("You have these roles:")
        for r in roles:
            print('- {}'.format(r))
        role = input("Pick a role : ")

    while role not in roles:
        role = input("The role you chose does not exist. Pick a valid role : ")
    
    profiles = helper_.get_profiles()
    info = {
            'profile': profile,
            'user': user,
            'role': role,
            'account': details['credentials_profile'][user][role]
            }
    if profile in profiles:
        helper_.write_file('state', info)
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
    creds = u.get_credentials(ctx.obj.current_state['user'])
    aws_creds, aws_config = u.create_config_parsers([ctx.obj.aws_creds_path, ctx.obj.aws_config_path])
    u.create_section(
        aws_creds,
        aws_config,
        ctx.obj.current_state['user'],
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
@click.option('--set')
@click.option('--get')
@click.option('--add-profile')
@click.option('--delete-profile')
@click.pass_context
def config(ctx, set, get, add_profile, delete_profile):
    helper_ = helper.Helper()
    u = Utility()
    if ctx.obj.profile:
        content = helper_.read_file("{}.prof".format(ctx.obj.profile))
        if set:
            key, value = set.split('=')
            if key.strip() in content.keys():
                content[key.strip()] = value.strip()
                helper_.write_file("{}.prof".format(ctx.obj.profile), content)
        elif get:
            if 'state' in get.strip():
                u.print_message(helper_.read_file('state'))
                state = helper_.read_file('state')
                for k,v in state.items():
                    u.print_message("{}: {}".format(k,v))
            elif get in content:
                u.print_message("The value for {} is {}".format(get, content[get]))
            else:
                u.print_message("There is no attribute : {}".format(get))
        elif add_profile:
            user, role_and_account = add_profile.split(".")
            role, account = role_and_account.strip().split(':')
            if user.strip() in content['credentials_profile']:
                content['credentials_profile'][user.strip()].update({role.strip(): account.strip()})
                helper_.write_file("{}.prof".format(ctx.obj.profile), content)
                u.print_message("New role `{}` added with account number `{}` for user `{}`".format(role, account, user))
            else:
                content['credentials_profile'][user.strip()] = {role.strip(): account.strip()}
                helper_.write_file("{}.prof".format(ctx.obj.profile), content)
                u.print_message("New user added `{}` withe role `{}` and account number `{}`".format(user, role, account))
        elif delete_profile:
            if "." in delete_profile:
                user, role = delete_profile.split(".")
                del content['credentials_profile'][user.strip()][role.strip()]
                helper_.write_file("{}.prof".format(ctx.obj.profile), content)
            else:
                del content['credentials_profile'][delete_profile.strip()]
                helper_.write_file("{}.prof".format(ctx.obj.profile), content)
    else:
        u = Utility()
        user_to_roles = {}
        u.print_message('Provide your configuration - leave blank for defaults in brackets')
        name = input("Configuration name [MyNewConfig] : ") or "MyNewConfig"
        config_path = input('AWS config path [~/.aws/config] : ') or '~/.aws/config'
        credentials_path = input('AWS credentials path [~/.aws/credentials] : ') or '~/.aws/credentials'
        token_duration = input('Duration of profile in seconds [86400 - one day] : ') or '86400'
        region = input('Region [eu-west-1] : ') or 'eu-west-1'
        output = input('Output [text] : ') or 'text'
        profiles = input('Profile to associate this configuration [default] (For multiple profiles separate by `,`): ') or 'default'
        # roles_and_accounts = input('Roles - accounts that you want to assume [Admin - 123456789]') or 'Admin - 123456789'

        for profile in profiles.split(','):
            user_to_roles[profile.strip()] = input("Provide a role and the account number for profile {} : ".format(profile.strip()))
        for k,v in user_to_roles.items():
            roles_and_accounts_pairs = v.split('-')
            user_to_roles[k] = {roles_and_accounts_pairs[0].strip(): roles_and_accounts_pairs[1].strip()}
        

        conf = ConfigureAwsAssumeRole(
            config_path=config_path,
            credentials_path=credentials_path,
            configuration_name=name,
            token_duration=token_duration,
            region=region,
            output=output,
            credentials_profile=profiles,
            roles_and_accounts=user_to_roles
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