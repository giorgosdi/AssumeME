import datetime
import os.path

import utils

class TimeHelper(object):

    def __init__(self, tz='utc', aws_credentials_path='~/.aws/credentials'):
        self.tz = tz
        self.aws_credentials_path = os.path.expanduser(aws_credentials_path)

    def _expiration_to_datetime(self, expiration):
        if isinstance(expiration, dict):
            expiration_time = datetime.datetime.strptime(
                expiration['aws_expiration'],
                '%Y-%m-%d %H:%M:%S%z'
            )
        else:
            expiration_time = datetime.datetime.strptime(
                expiration,
                '%Y-%m-%d %H:%M:%S%z'
            )
        return expiration_time

    def _find_timedelta(self, expiration_datetime):

        now_datetime = datetime.datetime.now(datetime.timezone.utc)
        # expiration_datetime = self._expiration_to_datetime(time)

        return  expiration_datetime - now_datetime