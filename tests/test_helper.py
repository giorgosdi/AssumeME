# from src.helper import Helper
from src.helper import Helper
import tempfile
import os
import yaml

class TestHelper(object):
    ASSUME_PATH = os.path.expanduser("~/.assume")
    helper = Helper()

    def remove_file(self, file_):
        os.remove(f"{os.path.expanduser('~/.assume')}/{file_}")
    
    def test_read_file(self):
        content = {"this": "is", "a": "test"}
        self.helper.write_file("test", content)
        
        assert isinstance(self.helper.read_file("test"), dict)
        assert self.helper.read_file("test") == content
        self.remove_file("test")
    
    def test_write_file(self):
        content = {"this": "is", "a": "test"}
        self.helper.write_file("test", content)
        written_content = self.helper.read_file("test")
        assert written_content == content
        self.remove_file("test")
    
    def test_get_profiles_zero_prof(self):
        profiles = self.helper.get_profiles()
        assert len(profiles) == 0

    def test_get_profiles_one_prof(self):
        content = {"this": "is", "a": "test"}
        self.helper.write_file("myprof.prof", content)
        profiles = self.helper.get_profiles()
        assert len(profiles) == 1
        self.remove_file("myprof.prof")