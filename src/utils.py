import configparser
import sys

import api
import logger


class Utility(object):
    def __init__(self):
        self.logger = logger.CustomLogger().create_logger()

    def print_message(self, message, error=''):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if not error:
            self.logger.info(message)
        else:
            self.logger.error("{} in line {}:\n{}".format(message, exc_tb.tb_lineno, error))

    def session_exists(self, section, credentials_path, config_path):
        if config_path.has_section(section):
            self.print_message('Section exists')
            return True
        else:
            self.print_message('Section not found')
            return False
    
    def get_credentials(self, section, profile):
        api_client = api.ApiCalls()
        sts_client = api_client.create_session(profile)
        return api_client.assume_role(profile, sts_client)

    def create_section(self, credentials, profile, section):
        credentials.add_section(section)

        