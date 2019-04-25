import os
import yaml

class Helper(object):
    def read_state_file(self,):
        if os.path.isfile(os.path.expanduser("~/.aws/state")):
            with open(os.path.expanduser("~/.aws/state")) as file_:
                content=yaml.load(file_, Loader=yaml.FullLoader)
        return content

    def write_state_file(self, content):
        with open(os.path.expanduser("~/.aws/state"), "w+") as file_:
            yaml.dump(content, file_, default_flow_style=False)

    def get_profiles(self,):
        files=[]
        for file_ in os.listdir(os.path.expanduser("~/.aws")):
            if ".prof" in file_:
                files.append(file_.split('.')[0])

        if files:
            for file_ in files:
                print("- {}".format(file_))
        return files
        

                