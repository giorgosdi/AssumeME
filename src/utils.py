import configparser
import sys
from os.path import expanduser
import datetime
import yaml
from random import randint
import os
from src.configure import ConfigureAwsAssumeRole

import src.logger as logger
import src.api_calls as api_calls
import src.time_helper as time_helper
import src.helper as helper
from src.section import Section


class Utility(object):
    def __init__(self):
        self.logger = logger.CustomLogger().create_logger()
        self.section = Section()


    def get_credentials(self, profile):
        helper_ = helper.Helper()
        api_client = api_calls.CustomApi()
        sts_client = api_client.create_session(profile)
        self.logger.print_message('STS session created')
        state = helper_.read_file('state')
        return api_client.assume_role(sts_client, state)

    def _write_option_to_config(self, parser, parser_path):
        with open(parser_path, 'w+') as parser_file:
            parser.write(parser_file)

    def _get_section_options(self, parser, section):
        return dict(parser[section])

    def _create_config_parsers(self, paths):
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

    def show_aws_profiles(self, profile_config, all, profile):
        credentials_path = expanduser(profile_config['credentials'])
        conf_path = expanduser(profile_config['config'])
        aws_credential_parser, aws_config_parser = self._create_config_parsers([credentials_path, conf_path])

        self.section._discover_sections(aws_credential_parser, all, profile)
    

    def create_file(self, path, file_):
        try:
            if os.path.exists(f"{path}/{file_}"):
                pass
            else:
                with open(f"{path}/{file_}", "w+"):
                    pass
        except Exception as error:
            print(f"The {file_} failed to be created with the following error : {error}")

    def create_directory(self, directory):
        try:
            if os.path.isdir(directory):
                pass
            else:

                os.mkdir(directory)
        except Exception as error:
            print(f"The {directory} failed to be created with the following error : {error}")
    
    def is_init(self):
        if os.path.isdir(expanduser("~/.assume")):
            if os.path.exists(expanduser("~/.assume/state")):
                initialise = True
            else:
                self.create_file("~/.assume", "state")
                initialise = True
        else:
            initialise = False
        return initialise


    def pick_from_list_of(self, kind, type_):
        print("Pick one from the following")
        [print(f"- {t}") for t in type_]
        choice = input("Choose one of the above : ")
        while choice not in type_:
            choice=input(f'This {kind} does not exist. Choose a {kind} from the list : ')
        return choice

if '__main__' in __name__:
    print('RUNNING UTILS')
    u = Utility()

    aws_creds_path=expanduser("~/.aws/credentials")
    aws_config_path=expanduser("~/.aws/config")
    aws_creds, aws_config = u.create_config_parsers([aws_creds_path, aws_config_path])

    # creds = u.get_credentials('test-user')
    # sections = u.discover_sections(aws_creds)
    # u.valid_sections(aws_creds, sections)
    u.clean_sections(aws_creds, aws_creds_path)
    # if u.section_exists('test-user-temp',aws_config):
    #     parser = u._set_section_options(aws_config, 'test-user-temp', {'region': 'eu-west-1'})
    #     u._write_option_to_config(parser, aws_config_path)
    # else:
    #     u.create_section(aws_creds, aws_config,'test-user', creds, aws_creds_path, aws_config_path)
