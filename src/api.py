import utils
import boto3

class ApiCalls(object):

    def create_session(self, profile):
        sts_session = boto3.Session(profile_name="{}".format(profile))
        sts = sts_session.client('sts')
        # self.section = '{}-temp'.format(profile)
        # self.profile_section = 'profile {}'.format(self.section)
        return sts

    def assume_role(self, profile, sts_client):
        # role_name, account_number = self.get_details_from_config(profile)
        print "Creating temporary credentials for " + colored("{}", 'green').format(profile) + " account..."
        creds = sts_client.assume_role(RoleArn='arn:aws:iam::{}:role/{}'.format(account_number, role_name), RoleSessionName="temporary-role-{}-{}".format(profile, role_name) )
        return creds