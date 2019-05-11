import boto3

class CustomApi(object):

    def create_session(self, profile):
        sts_session = boto3.Session(profile_name="{}".format(profile))
        sts = sts_session.client('sts')
        return sts

    def assume_role(self, sts_client, state):
        creds = sts_client.assume_role(RoleArn='arn:aws:iam::{}:role/{}'.format(state['account'], state['role']), RoleSessionName="temporary-role-{}-{}".format(state['profile'], state['role']) )
        return creds