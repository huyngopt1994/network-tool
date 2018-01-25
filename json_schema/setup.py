from setuptools import setup, find_packages

VERSION="0.0.0"
DESCR = "json_schema validator for python"
LONG_DESCR = """
jsonschema is written in pure python and currently has no dependencies.

Validators may be subclassed much like simplejson encoders to provide
speical functionality or extensions. 
"""
setup(name="json_schema",
      version=VERSION,
      description=DESCR,
      long_description=LONG_DESCR)