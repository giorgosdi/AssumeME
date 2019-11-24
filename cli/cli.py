import click
from src.configure import ConfigureAwsAssumeRole
from src.utils import Utility
import src.helper as helper

from os.path import expanduser
import os
import yaml

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
    if os.path.isdir(f"{APPLICATION_HOME_DIR}"):
        u = Utility()
        helper_ = helper.Helper()
        if os.path.isfile(f"{APPLICATION_HOME_DIR}/state"):
            pass
        else:
            u.create_file(APPLICATION_HOME_DIR, "state")

        content = helper_.read_file('state')
        profiles = helper_.get_profiles()
        if content is not None:
            if content.get('profile'):
                ctx.obj = ConfigSetup(content['profile'])
                
        elif profiles:
            print("You already have a profile configured..")
            profile = u.pick_from_list_of("profile", profiles)
            profile_content = helper_.read_file(f"{profile}.prof")

            users = list(profile_content['credentials_profile'].keys())
            user = u.pick_from_list_of("user", users)

            roles = list(profile_content['credentials_profile'][user].keys())
            role = u.pick_from_list_of("role", roles)
            state_content ={
                'profile': profile,
                'account': profile_content['credentials_profile'][user][role],
                'user': user,
                'role': role
            }
            helper_.write_file("state", state_content)
        else:
            conf = u.configure()
            conf.create_config(conf.config)     
    else:
        print("Initializing..")
        init(ctx)
        config(ctx)
       
# def temp():
#     else:
#         print("State file does not exists.")
#         profiles = helper_.get_profiles()
#         if profiles:
#             profile=input('Choose one of these profiles : ')
#             while profile not in profiles:
#                 profile=input('This profile does not exist. Choose a profile from the list above : ')
#             content = helper_.read_file('{}.prof'.format(profile))
#             profile_ = content['profile']
#             user_ = list(content['credentials_profile'].keys())[0]
#             role_ = list(content['credentials_profile'][user_].keys())[0]
#             account_ = content['credentials_profile'][user_][role_]
#             helper_.write_file('state', {
#                     'profile': profile_,
#                     'user': user_,
#                     'role': role_,
#                     'account': account_
#                 })
#             ctx.obj = ConfigSetup(profile)
#         else:
#             print("There are no profiles available, you should create a new profile.")
#             config()

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
                    u = Utility()
                    profile = ConfigSetup(content['profile'])
                    parsers = {
                        "config": ctx.obj.aws_config,
                        "credentials": ctx.obj.aws_creds
                    }
                    paths = {
                        "config": ctx.obj.aws_config_path,
                        "credentials": ctx.obj.aws_creds_path
                    }
                    u.clean_sections(parsers, paths)



@actions.command(help="Configure a new profile with your prefered settings.")
@click.option('--set')
@click.option('--get')
@click.option('--add-profile')
@click.option('--delete-profile')
@click.pass_context
def config(ctx, set, get, add_profile, delete_profile):
    helper_ = helper.Helper()
    u = Utility()

    if u.is_init():
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
            conf = u.configure()
            conf.create_config(conf.config)
    else:
        actions()

@actions.command(help="Initialise asm")
@click.pass_context
def init(ctx):
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
        print("Good news, `asm` is already initialised !")

    if not directory:
        u.create_directory(APPLICATION_HOME_DIR)
        u.create_file(APPLICATION_HOME_DIR, "state")
        state = True
        print("Initialization was successful..")
    if not state:
        u.create_file("state")

@actions.command(help="You are using it right now")
@click.pass_context
def help(ctx):
    print(actions.get_help(ctx))

@actions.command(help="Print the command to export the AWS profile")
@click.pass_context
def export(ctx):
    print(f"export AWS_PROFILE={ctx.obj.profile}")

def main():
    actions()
# if __name__ == '__main__':
#     actions()