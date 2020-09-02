import sys

import logging

class CustomLogger(object):

    def __init__(self, level=logging.DEBUG, log_format='%(asctime)s - %(name)s:__%(levelname)s__: %(message)s'):
      self.level = level
      self.log_format = log_format
      self.logger = self.create_logger()

    def create_logger(self):
      logging.basicConfig(format=self.log_format)
      logger = logging.getLogger(__name__)
      logger.setLevel(self.level)
      return logger

    def print_message(self, message, error=''):
      exc_type, exc_obj, exc_tb = sys.exc_info()
      if not error:
        self.logger.info(message)
      else:
        self.logger.error("{} in line {}:\n{}".format(message, exc_tb.tb_lineno, error))