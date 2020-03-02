import configparser
import ruamel.yaml
from os.path import expanduser

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

    def create_config(self, configuration):
        try:
            with open("{}/{}.prof".format(self.application_home_dir, self.config_name), "w+") as f:
                f.write(ruamel.yaml.dump(configuration, default_flow_style=False))
            print("Configuration created successfully : {}/{}".format(self.application_home_dir, self.config_name))
        except Exception as e:
            print(e)