import configparser
import sys
from os.path import expanduser
import datetime
import yaml
from random import randint

import src.logger as logger
import src.api_calls as api_calls
import src.time_helper as time_helper
import src.helper as helper


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

    def section_exists(self, section, config_path):
        found = False
        if config_path.has_section(section):
            self.print_message('Section exists')
            found=True
        elif config_path.has_section("profile {}".format(section)):
            self.print_message("Section exists")
            found = True
        else:
            self.print_message('Section not found')
            found = False
        return found

    def get_credentials(self, profile):
        helper_ = helper.Helper()
        api_client = api_calls.CustomApi()
        sts_client = api_client.create_session(profile)
        self.print_message('STS session created')
        state = helper_.read_file('state')
        return api_client.assume_role(sts_client, state)

    def create_section(self, aws_credential_parser, aws_config_parser, profile, creds, credentials_path, conf_path):
        self.print_message(profile)

        if self.section_exists("{}-temp".format(profile), aws_credential_parser):
            self.print_message('Section already exists')
            answer = input("Do you want to overwrite the existing temporary credentials ? [y/N] : ")

            if answer.lower() in ['y', 'yes']:
                section = "{}-temp".format(profile)
                self.apply_section("{}".format(section), aws_credential_parser, credentials_path, creds, 'update')
                self.print_message("Profile created with name {}".format(profile))
            else:
                section = "{}-{}".format(profile, randint(1000, 9999))
                self.print_message("Attaching a random 4-letter string in the of your profile")
                self.apply_section(section, aws_credential_parser, credentials_path, creds, 'create')
                self.print_message("Profile created with name {}".format("{}-{}".format(profile, section)))

        else:
            section = "{}-temp".format(profile)
            self.print_message('Creating temporary credentials')
            self.apply_section(section, aws_credential_parser, credentials_path, creds, 'create')
            self.print_message('Credentials have been created under profile : {}'.format(profile))
        if self.section_exists("{}-temp".format(profile), aws_config_parser):
            self.print_message("Profile exists in the AWS config. No further action needed")
        else:
            self.print_message('Adding a section in `config` file for the new temp-role')
            self.apply_section("profile {}".format(section), aws_config_parser, conf_path, {'region': 'eu-west-1', 'output': 'table'}, 'create')
            self.print_message('Section added')

    def apply_section(self, section, parser, parser_path, details, action):
        if 'create' in action.lower():
            parser.add_section(section)
        if 'Credentials' in details.keys():
            self._set_section_options(parser, section, details['Credentials'])
        else:
            self._set_section_options(parser, section, details)

        self._write_option_to_config(parser, parser_path)

    def _set_section_options(self, parser, section, details):
        helper = time_helper.TimeHelper()
        for key, value in details.items():
            if key in self._credentials_mapping.keys():
                parser.set(section, self._credentials_mapping[key], helper._datetime_to_string(value) if isinstance(value, datetime.datetime) else value)
            else:
                parser.set(section, key, value)
        return parser

    def _write_option_to_config(self, parser, parser_path):
        with open(parser_path, 'w+') as parser_file:
            parser.write(parser_file)

    def _get_section_options(self, parser, section):
        return dict(parser[section])

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


    def discover_sections(self, parser, all, profile):
        sections = parser.sections()
        sections_discovered=[]
        if all:
            for section in sections:
                if parser.has_option(section, 'aws_expiration'):
                    helper = time_helper.TimeHelper()
                    expiration = parser.get(section, 'aws_expiration')

                    time = helper._expiration_to_datetime(expiration)

                    sections_discovered.append(section)
                    self.print_message('Section {} with expiration date {}'.format(section, time))
        else:
            for section in sections:
                if profile in section:
                    if parser.has_option(section, 'aws_expiration'):
                        helper = time_helper.TimeHelper()
                        expiration = parser.get(section, 'aws_expiration')

                        time = helper._expiration_to_datetime(expiration)

                        sections_discovered.append(section)
                        self.print_message('Section {} with expiration date {}'.format(section, time))
        return sections_discovered


    def valid_sections(self, parser, sections):
        for section in sections:
            timedelta = self._is_section_valid(parser,section)
            if timedelta:
                self.print_message('You have {} left for your {} role'.format(timedelta, section))


    def _is_section_valid(self, parser, section):
        if parser.has_option(section, 'aws_expiration'):
            helper = time_helper.TimeHelper()
            expiration = parser.get(section, 'aws_expiration')

            time = helper._expiration_to_datetime(expiration)
            timedelta = helper._find_timedelta(time)
            return timedelta if timedelta.total_seconds()>0 else False

    def clean_sections(self, parsers, parser_paths):
        sections_to_be_removed=[]
        config_sections = parsers['config'].sections()
        credentials_sections = parsers['credentials'].sections()
        for section in config_sections:
            if parsers['config'].has_option(section, 'aws_expiration'):
                timedelta = self._is_section_valid(parsers['config'], section)
                if timedelta:
                    choice = input("Do you want to remove section {} - It is still valid for {} : ".format(section, timedelta))
                    if 'y' in choice.lower():
                        parsers['config'].remove_section(section)
                        parsers['credentials'].remove_section(section)
                        sections_to_be_removed.append(section)
                    else:
                        self.print_message('Profile skipped')
            else:
                parsers['config'].remove_section(section)
                parsers['credentials'].remove_section(section)
                sections_to_be_removed.append(section)

        self._write_option_to_config(parsers['config'], parser_paths['config'])
        self._write_option_to_config(parsers['credentials'], parser_paths['credentials'])
        [ self.print_message("Section removed : {}".format(section)) for section in sections_to_be_removed ]
    
    def read_configuration(self, profile):
        with open(expanduser("~/.assume/{}.prof".format(profile))) as f:
            return yaml.load(f, Loader=yaml.FullLoader)


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
