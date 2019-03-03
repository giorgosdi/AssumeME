import configparser
import sys
from os.path import expanduser

import logger
import api_calls


class Utility(object):
    def __init__(self):
        self.logger = logger.CustomLogger().create_logger()
        self._credentials_mapping = {
            "AccessKeyId":"aws_access_key_id",
            "SecretAccessKey": "aws_secret_access_key",
            "SessionToken": "aws_session_token",
            "Expiration": "aws_expiration"
        }

    def print_message(self, message, error=''):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if not error:
            self.logger.info(message)
        else:
            self.logger.error("{} in line {}:\n{}".format(message, exc_tb.tb_lineno, error))

    def session_exists(self, section, config_path):
        if config_path.has_section(section):
            self.print_message('Section exists')
        else:
            self.print_message('Section not found')
        return True if config_path.has_section(section) else  False
    
    def get_credentials(self, profile):
        api_client = api_calls.CustomApi()
        sts_client = api_client.create_session(profile)
        self.print_message('STS session created')
        return api_client.assume_role(profile, sts_client)

    def create_section(self, aws_credential, aws_config, profile, creds, credentials_path, conf_path):
        
        self.print_message('Creating temporary credentials')
        self.add_section(profile, aws_credential, credentials_path, creds)
        self.print_message('Credentials have been created under profile : {}'.format(profile))

        self.print_message('Adding a section in `config` file for the new temp-role')
        self.add_section(profile, aws_config, conf_path, {'region': 'eu-west-1', 'output': 'table'} )
        self.print_message('Section added')

    def add_section(self, profile, parser, parser_path, details):
        section = "{}-temp".format(profile)
        parser.add_section(section)
        if 'Credentials' in details.keys():
            self._set_section_options(parser, section, details['Credentials'])
        else:
            self._set_section_options(parser, section, details)

        self._write_option_to_config(parser, parser_path)

    def _set_section_options(self, parser, section, details):
        for key, value in details.items():
            if key in self._credentials_mapping.keys():
                parser.set(section, self._credentials_mapping[key], str(value))
            else:
                parser.set(section, key, value)
        return parser

    def _write_option_to_config(self, parser, parser_path):
        with open(parser_path, 'w+') as parser_file:
            parser.write(parser_file)
    
    def create_config_parsers(self, paths):
        list_of_parsers = []
        if isinstance(paths, list):
            for path in paths:
                if 'aws' in path:
                    if 'credentials' in path:
                        credentials_parser = configparser.ConfigParser()
                        credentials_parser.read([path])
                        list_of_parsers.append(credentials_parser)
                    else:
                        config_parser = configparser.ConfigParser()
                        config_parser.read([path])
                        list_of_parsers.append(config_parser)
        else:
            generic_parser = configparser.ConfigParser()
            generic_parser.read([paths])
            list_of_parsers.append(generic_parser)
        return list_of_parsers if len(list_of_parsers) > 0 else list_of_parsers[0]
                
if '__main__' in __name__:
    print('RUNNING UTILS')
    u = Utility()

    aws_creds_path=expanduser("~/.aws/credentials")
    aws_config_path=expanduser("~/.aws/config")
    aws_creds, aws_config = u.create_config_parsers([aws_creds_path, aws_config_path])

    creds=u.get_credentials('test-user')
    if u.session_exists('test-user-temp',aws_config):
        parser = u._set_section_options(aws_config, 'test-user-temp', {'region': 'eu-west-1'})
        u._write_option_to_config(parser, aws_config_path)
    else:
        u.create_section(aws_creds, aws_config,'test-user', creds, aws_creds_path, aws_config_path)