import boto3

class CustomApi(object):

    def create_session(self, profile):
        sts_session = boto3.Session(profile_name="{}".format(profile))
        sts = sts_session.client('sts')
        # self.section = '{}-temp'.format(profile)
        # self.profile_section = 'profile {}'.format(self.section)
        return sts

    def assume_role(self, sts_client, state):
        # role_name, account_number = self.get_details_from_config(profile)
        # print("Creating temporary credentials for " + colored("{}", 'green').format(profile) + " account...")
        creds = sts_client.assume_role(RoleArn='arn:aws:iam::{}:role/{}'.format(state['account'], state['role']]), RoleSessionName="temporary-role-{}-{}".format(state['profile'], state['role']) )
        return creds