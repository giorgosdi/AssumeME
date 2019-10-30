from setuptools import setup, find_packages
import os

home = os.path.expanduser("~")

setup(name='asm',
      version='0.2.5',
      description='Easy and simple role assumption for AWS',
      author='Giorgos Dimitriou',
      author_email='giwrgosdi@gmail.com',
      packages=find_packages(),
      install_requires=[
	'click',
	'boto3',
	'ConfigParser',
      'PyYAML',
      'ruamel.yaml'
      ],
      include_package_data=True,
      data_files=[(
            '{}/.assume'.format(home),["state"]
      )],
      entry_points={
            'console_scripts': [
                  'asm = cli.cli:main',
            ],
      },
      classifiers=[
            "Programming Language :: Python :: 3",
            "Environment :: Console",
      ]
     )
