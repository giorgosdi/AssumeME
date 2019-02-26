import configparser
import ruamel.yaml
from os.path import expanduser

class ConfigureAwsAssumeRole(object):
    """docstring for ConfigureAwsAssumeRole."""
    def __init__(self, config_path="~/.aws/config", credentials_path="~/.aws/credentials",
        configuration_name="mydefaultprofile", token_duration=3600, region="eu-west-1", output="test", credentials_profile="mydefaultprofile"):
        super(ConfigureAwsAssumeRole, self).__init__()
        self.aws_config_path = expanduser(config_path)
        self.aws_credentials_path = expanduser(credentials_path)
        self.aws_path = f"{self.aws_config_path.split('aws')[0]}aws"
        self.config_name = f"{ configuration_name }"
        self.config = {
            'name': self.config_name,
            'config': self.aws_config_path,
            'credentials': self.aws_credentials_path,
            'duration': token_duration,
            'region': region,
            'output': output,
            'credentials_profile': credentials_profile
        }

    def create_configuration_dictionary(self):
        return {
            f"{ self.config_name }": self.config
        }

    def create_config(self, configuration):
        try:
            with open("{}/{}.yaml".format(self.aws_path, self.config_name), "w+") as f:
                f.write(ruamel.yaml.dump(configuration, default_flow_style=False))
            print(f"Configuration created successfully : { self.aws_path }/{ self.config_name }")
        except Exception as e:
            print(e)