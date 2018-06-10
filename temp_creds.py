from os.path import expanduser
from termcolor import cprint, colored
import boto3
import ConfigParser
import argparse


class TempCreds(object):
    """
    docstring for TempCreds
    """
    home = expanduser("~")

    aws_creds = ConfigParser.ConfigParser()
    creds_path = "{}/.aws/credentials".format(home)
    creds_file_path = expanduser(creds_path)
    aws_creds.read([creds_file_path])

    aws_config = ConfigParser.ConfigParser()
    config_path = "{}/.aws/config".format(home)
    config_file_path = expanduser(config_path)
    aws_config.read([config_file_path])

    access_key = 'aws_access_key_id'
    secret_key = 'aws_secret_access_key'
    token = 'aws_session_token'

    def __init__(self, profile):
        sts_session = boto3.Session(profile_name="{}".format(profile))
        self.sts = sts_session.client('sts')
        self.section = '{}-temp'.format(profile)
        self.profile_section = 'profile {}'.format(self.section)

    def return_cred_list(self, profile):
        if self.aws_creds.has_section(self.section):
            try:
                print "Section found !"
            except Exception as e:
                print e
        else:
            print colored("There are no temporary credentials for this profile", "red", attrs=['bold'])
            print "Creating a section for this profile.."
            self.aws_creds.add_section(self.section)
            self.aws_config.add_section(self.profile_section)
            self.aws_creds.set(self.section, self.access_key, 'placeholder')
            self.aws_creds.set(self.section, self.secret_key, 'placeholder')
            self.aws_creds.set(self.section, self.token, 'placeholder')


        existing_access_key = self.aws_creds.get(self.section, self.access_key)
        existing_secret_key = self.aws_creds.get(self.section, self.secret_key)
        existing_token = self.aws_creds.get(self.section, self.token)

        return existing_access_key, existing_secret_key, existing_token

    def get_details_from_config(self, profile):
        if self.aws_config.has_section("profile {}".format(profile)):
            role_arn = self.aws_config.get("profile {}".format(profile), "role_arn")
            role_name = role_arn.split('/')[1]
            account_number = role_arn.split(':')[4]
            return role_name, account_number

    def get_temp_creds(self, profile):
        role_name, account_number = self.get_details_from_config(profile)
        print "Creating temporary credentials for " + colored("{}", 'green').format(profile) + " account..."
        creds = self.sts.assume_role(RoleArn='arn:aws:iam::{}:role/{}'.format(account_number, role_name), RoleSessionName="giorgos-{}-{}".format(profile, role_name) )
        return creds

    def main(self, profile):


        existing_access_key, existing_secret_key, existing_token = self.return_cred_list(profile)


        print "Existing access key : " + colored("{}".format(existing_access_key), 'blue', attrs=['bold'])
        print "Existing secret key : " + colored("{}".format(existing_secret_key), 'blue', attrs=['bold'])

        new_creds = self.get_temp_creds(profile)

        print "Writing new credentials to file.."
        self.aws_creds.set(self.section, self.access_key, new_creds['Credentials']['AccessKeyId'])
        self.aws_creds.set(self.section, self.secret_key, new_creds['Credentials']['SecretAccessKey'])
        self.aws_creds.set(self.section, self.token, new_creds['Credentials']['SessionToken'])
        with open(self.creds_file_path, 'wb') as configfile:
            self.aws_creds.write(configfile)


        if not self.aws_config.has_section(self.profile_section):
            print "Creating profile in config.."
            output = self.aws_config.get("profile {}".format(profile), 'output')
            region = self.aws_config.get("profile {}".format(profile), 'region')
            self.aws_config.add_section(self.profile_section)
            self.aws_config.set(self.profile_section, 'output', output)
            self.aws_config.set(self.profile_section, 'region', region)
            with open(self.config_file_path, 'wb') as config:
                self.aws_config.write(config)


        print "New access key : " + colored("{}".format(new_creds['Credentials']['AccessKeyId']), 'green')
        print "New secret key : " + colored("{}".format(new_creds['Credentials']['SecretAccessKey']), 'green')
        print "New token : " + colored("{}".format(new_creds['Credentials']['SessionToken']), 'green')
        for i in range(1,5):
            print "." * i
        print "Temporary credentials created under " + colored("{}-temp ", 'magenta', attrs=['bold']).format(profile) + "profile"
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create temporary credentials')
    parser.add_argument('-p', '--profile', action="store", help="The profile you want to use to assume a role", required=True, type=str)
    args = parser.parse_args()

    profile = args.profile
    print "Profile given: " + colored("{}".format(profile), 'green')

    p = TempCreds(profile)
    p.main(profile)
