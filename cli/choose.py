import click

from src.utils import Utility
import src.helper as helper

@click.command(name="choose", help="Choose a profile and add it in your state file")
@click.argument('profile')
@click.option('--role')
@click.option('--user')
@click.pass_context
def choose_command(ctx, profile, user, role):
    u = Utility()
    if u.is_init():
        helper_ = helper.Helper()
        existing_profiles = helper_.get_profiles()
        while profile not in existing_profiles:
            profile = u.pick_from_list_of("profile", existing_profiles)

        details = helper_.read_file("{}.prof".format(profile))
        users = details.get('credentials_profile', None)
        if users is not None:
            users = list(users.keys())
        else:
            print("Malformed state file. The profile has no users") 
            exit(1)
        
        user = u.pick_from_list_of("user", users)
        
        roles = details.get('credentials_profile', None).get(user, None)
        if roles is not None:
            roles = list(roles.keys())
        else:
            print("Malformed state file. The profile has no roles") 
            exit(1)
        role = u.pick_from_list_of("role", roles)
        
        info = {
                'profile': profile,
                'user': user,
                'role': role,
                'account': details['credentials_profile'][user][role]
                }

        helper_.write_file('state', info)
    else:
        print("You need to initialize first.")


