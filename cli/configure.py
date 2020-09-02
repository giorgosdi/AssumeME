import click

from src.utils import Utility
import src.helper as helper

@click.command(name="config", help="Configure a new profile with your prefered settings.")
@click.option('--set')
@click.option('--get')
@click.option('--add-profile')
@click.option('--delete-profile')
@click.pass_context
def configure_command(ctx, set, get, add_profile, delete_profile):
  helper_ = helper.Helper()
  u = Utility()
  content = helper_.read_file("state")
  if u.is_init():
    if content is not None:
      if content.get("profile"):
        profile_config = helper_.read_file("{}.prof".format(content["profile"]))
        if set:
          key, value = set.split('=')
          if key.strip() in profile_config.keys():
            profile_config[key.strip()] = value.strip()
            helper_.write_file("{}.prof".format(content["profile"]))
        elif get:
          if 'state' in get.strip():
            u.print_message(helper_.read_file('state'))
            state = helper_.read_file('state')
            for k,v in state.items():
              u.print_message("{}: {}".format(k,v))
          elif get in profile_config:
            u.print_message("The value for {} is {}".format(get, profile_config[get]))
          else:
            u.print_message("There is no attribute : {}".format(get))
        elif add_profile:
          user, role_and_account = add_profile.split(".")
          role, account = role_and_account.strip().split(':')
          if user.strip() in profile_config['credentials_profile']:
            profile_config['credentials_profile'][user.strip()].update({role.strip(): account.strip()})
            helper_.write_file("{}.prof".format(content["profile"]), profile_config)
            u.print_message("New role `{}` added with account number `{}` for user `{}`".format(role, account, user))
          else:
            profile_config['credentials_profile'][user.strip()] = {role.strip(): account.strip()}
            helper_.write_file("{}.prof".format(content["profile"]), profile_config)
            u.print_message("New user added `{}` with role `{}` and account number `{}`".format(user, role, account))
        elif delete_profile:
          if "." in delete_profile:
            user, role = delete_profile.split(".")
            del profile_config['credentials_profile'][user.strip()][role.strip()]
            helper_.write_file("{}.prof".format(content["profile"]), profile_config)
          else:
            del profile_config['credentials_profile'][delete_profile.strip()]
            helper_.write_file("{}.prof".format(content["profile"]), profile_config)
    else:
        conf = u.configure()
        conf.create_config(conf.config)
  else:
      print("You need to initialize first.")