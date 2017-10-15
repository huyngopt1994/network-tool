import os
from setuptools import setup

with open('requirement') as f :
    required = f.read().splitlines()

setup(
    name = 'NetWork Utils',
    version=  '0.0.0',
    author= 'Huy Ngo',
    author_email = 'huyngopt1994@gmail.com',
    description= 'Where store a lot of tools for network wrote by python',
    install_requires = required
)