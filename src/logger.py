import logging

class CustomLogger(object):

    def __init__(self, level=logging.DEBUG, log_format='%(asctime)s - %(name)s:__%(levelname)s__: %(message)s'):
        self.level = level
        self.log_format = log_format

    def create_logger(self):
        logging.basicConfig(format=self.log_format)
        logger = logging.getLogger(__name__)
        logger.setLevel(self.level)
        return logger