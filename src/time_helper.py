import datetime
from dateutil import parser
import os.path

import src.utils as utils

class TimeHelper(object):

    def __init__(self, tz='utc', aws_credentials_path='~/.aws/credentials'):
        self.tz = tz
        self.aws_credentials_path = os.path.expanduser(aws_credentials_path)

    def _string_to_datetime(self, string):
        return parser.parse(string)
        # return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S%z")

    def _datetime_to_string(self, date):
        return datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S%z")

    def _expiration_to_datetime(self, expiration):
        if isinstance(expiration, dict):
            date_time = self._string_to_datetime(expiration['aws_expiration'])
        else:
            date_time = self._string_to_datetime(expiration)

        return date_time

    def _find_timedelta(self, expiration_datetime):

        now_datetime = datetime.datetime.now(datetime.timezone.utc)
        return  expiration_datetime - now_datetime
