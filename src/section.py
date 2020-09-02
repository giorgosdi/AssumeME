from os.path import expanduser

import src.time_helper as time_helper
from src.logger import CustomLogger

class Section(object):
  def __init__(self):
    self.logger = CustomLogger()
    self._credentials_mapping = {
        "AccessKeyId":"aws_access_key_id",
        "SecretAccessKey": "aws_secret_access_key",
        "SessionToken": "aws_session_token",
        "Expiration": "aws_expiration"
    }

  def _discover_sections(self, parser, all, profile):
      sections = parser.sections()
      sections_discovered=[]
      if all:
        for section in sections:
          if parser.has_option(section, 'aws_expiration'):
            helper = time_helper.TimeHelper()
            expiration = parser.get(section, 'aws_expiration')

            time = helper._expiration_to_datetime(expiration)

            sections_discovered.append(section)
            self.logger.print_message('Section {} with expiration date {}'.format(section, time))
      else:
        for section in sections:
          if profile in section:
            if parser.has_option(section, 'aws_expiration'):
              helper = time_helper.TimeHelper()
              expiration = parser.get(section, 'aws_expiration')

              time = helper._expiration_to_datetime(expiration)

              sections_discovered.append(section)
              self.logger.print_message('Section {} with expiration date {}'.format(section, time))
      return sections_discovered

  def _is_section_valid(self, parser, section):
    if parser.has_option(section, 'aws_expiration'):
      helper = time_helper.TimeHelper()
      expiration = parser.get(section, 'aws_expiration')

      time = helper._expiration_to_datetime(expiration)
      timedelta = helper._find_timedelta(time)
      return timedelta if timedelta.total_seconds()>0 else False

  def _set_section_options(self, parser, section, details):
    helper = time_helper.TimeHelper()
    for key, value in details.items():
      if key in self._credentials_mapping.keys():
        parser.set(section, self._credentials_mapping[key], helper._datetime_to_string(value) if isinstance(value, datetime.datetime) else value)
      else:
        parser.set(section, key, value)
    return parser


    def _apply_section(self, section, parser, parser_path, details, action):
      if 'create' in action.lower():
        parser.add_section(section)
      if 'Credentials' in details.keys():
        self._set_section_options(parser, section, details['Credentials'])
      else:
        self._set_section_options(parser, section, details)
      self._write_option_to_config(parser, parser_path)

    def section_exists(self, section, config_path):
      found = False
      if config_path.has_section(section):
        self.logger.print_message('Section exists')
        found=True
      elif config_path.has_section("profile {}".format(section)):
        self.logger.print_message("Section exists")
        found = True
      else:
        self.logger.print_message('Section not found')
        found = False
      return found

    # Currently not being used
    def valid_sections(self, parser, sections):
      for section in sections:
        timedelta = self._is_section_valid(parser,section)
        if timedelta:
          self.logger.print_message('You have {} left for your {} role'.format(timedelta, section))

    # TODO: Fix clean_sections (it deletes all entries in config)
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
              self.logger.print_message('Profile skipped')
        else:
          parsers['config'].remove_section(section)
          parsers['credentials'].remove_section(section)
          sections_to_be_removed.append(section)

      self._write_option_to_config(parsers['config'], parser_paths['config'])
      self._write_option_to_config(parsers['credentials'], parser_paths['credentials'])
      [ self.logger.print_message("Section removed : {}".format(section)) for section in sections_to_be_removed ]

    def create_section(self, profile_config, profile, creds):
      credentials_path = expanduser(profile_config['credentials'])
      conf_path = expanduser(profile_config['config'])
      aws_credential_parser, aws_config_parser = self._create_config_parsers([credentials_path, conf_path])
      
      self.logger.print_message(profile)

      if self.section_exists("{}-temp".format(profile), aws_credential_parser):
        self.logger.print_message('Section already exists')
        answer = input("Do you want to overwrite the existing temporary credentials ? [y/N] : ")

        if answer.lower() in ['y', 'yes']:
          section = "{}-temp".format(profile)
          self._apply_section("{}".format(section), aws_credential_parser, credentials_path, creds, 'update')
          self.logger.print_message("Profile created with name {}".format(profile))
        else:
          section = "{}-{}".format(profile, randint(1000, 9999))
          self.logger.print_message("Attaching a random 4-letter string in the of your profile")
          self._apply_section(section, aws_credential_parser, credentials_path, creds, 'create')
          self.logger.print_message("Profile created with name {}".format("{}-{}".format(profile, section)))

      else:
        section = "{}-temp".format(profile)
        self.logger.print_message('Creating temporary credentials')
        self._apply_section(section, aws_credential_parser, credentials_path, creds, 'create')
        self.logger.print_message('Credentials have been created under profile : {}'.format(profile))

      if self.section_exists("{}-temp".format(profile), aws_config_parser):
        self.logger.print_message("Profile exists in the AWS config. No further action needed")
      else:
        self.logger.print_message('Adding a section in `config` file for the new temp-role')
        self._apply_section("profile {}".format(section), aws_config_parser, conf_path, {'region': 'eu-west-1', 'output': 'table'}, 'create')
        self.logger.print_message('Section added')
      