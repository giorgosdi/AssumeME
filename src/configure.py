import configparser
import ruamel.yaml
from os.path import expanduser

from logger import CustomLogger

APPLICATION_HOME_DIR = expanduser("~/.assume")

class ConfigureAwsAssumeRole(object):
    """docstring for ConfigureAwsAssumeRole."""
    def __init__(self, config_path="~/.aws/config", credentials_path="~/.aws/credentials",
        configuration_name="mydefaultprofile", token_duration=3600, region="eu-west-1", output="test", credentials_profile="mydefaultprofile", roles_and_accounts={}):
        super(ConfigureAwsAssumeRole, self).__init__()
        self.aws_config_path = expanduser(config_path)
        self.aws_credentials_path = expanduser(credentials_path)
        self.application_home_dir = expanduser("~/.assume")
        self.config_name = configuration_name
        self.config = {
            'name': self.config_name,
            'config': self.aws_config_path,
            'credentials': self.aws_credentials_path,
            'duration': token_duration,
            'region': region,
            'output': output,
            'credentials_profile': roles_and_accounts
        }
        self.logger = CustomLogger()

    def create_config(self, configuration):
        try:
            with open("{}/{}.prof".format(self.application_home_dir, self.config_name), "w+") as f:
                f.write(ruamel.yaml.dump(configuration, default_flow_style=False))
            print("Configuration created successfully : {}/{}".format(self.application_home_dir, self.config_name))
        except Exception as e:
            print(e)

    def configure(self):
        user_to_roles = {}
        self.logger.print_message('Provide your configuration - leave blank for defaults in brackets')
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
        return conf