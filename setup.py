from setuptools import setup, find_packages,find_namespace_packages
import os

home = os.path.expanduser("~")

setup(name='Assume role',
      version='0.1',
      description='Easy and simple role assumtion for AWS',
      author='Giorgos Dimitriou',
      author_email='giwrgosdi@gmail.com',
      packages=find_packages(),
      # package_dir={'': 'src'},
      # packages=find_namespace_packages(where='src'),
      install_requires=[
	'click',
	'boto3',
	'ConfigParser',
      'PyYAML',
      'ruamel.yaml'
      # 'python_version>=3'
      ],
      include_package_data=True,
      data_files=[(
            '{}/.assume'.format(home),["state"]
      )],
      entry_points={
            'console_scripts': [
                  'asm = cli.cli:main',
            ],
      }
     )
