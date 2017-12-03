from setuptools import setup, find_packages
import server

setup(name="ftp-utils",
      version=server.__version__,
      description="Ftp test utilities",
      author="HuyNgo",
      author_email="huyngopt1994@gmail.com",
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          "console_scripts": [
              "ftp-server = server:server:main",
          ]
      }
)