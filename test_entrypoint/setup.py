from setuptools import setup

with open('version.py') as f:
    exec (f.read())

setup(
    name="test_entrypoint",
    version=__version__,
    entry_points= {
        'console_scripts': [
            'test_entrypoint=main:main',
        ]
    }
)
