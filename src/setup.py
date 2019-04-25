from setuptools import setup
import os

home = os.path.expanduser("~")

setup(name='Assume role',
      version='0.1',
      description='Easy and simple role assumtion for AWS',
      author='Giorgos Dimitriou',
      author_email='giwrgosdi@gmail.com',
      # url='https://www.python.org/sigs/distutils-sig/',
      packages=['src'],
      # data_files=[(
      #       '{}/.assume'.format(home), [
      #             "{}/.assume/state".format(home)
      #       ]
      # )],
      data_files=[
            ('assume')
      ],
      entry_points={
            'console_scripts': [
                  'assume = cli:main',
            ],
      }
     )