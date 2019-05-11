import os
import yaml

class Helper(object):
    def read_file(self, file_):
        if os.path.isfile(os.path.expanduser("~/.assume/{}".format(file_))):
            with open(os.path.expanduser("~/.assume/{}".format(file_))) as f:
                content=yaml.load(f, Loader=yaml.FullLoader)
            return content

    def write_file(self, file_, content):
        with open(os.path.expanduser("~/.assume/{}".format(file_)), "w+") as f:
            yaml.dump(content, f, default_flow_style=False)

    def get_profiles(self,):
        files=[]
        for file_ in os.listdir(os.path.expanduser("~/.assume")):
            if ".prof" in file_:
                files.append(file_.split('.')[0])
        return files
        

                