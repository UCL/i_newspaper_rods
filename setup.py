import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "iNewsRods",
    version = "0.0.1",
    author = "James Hetherington",
    author_email = "j.hetherington@ucl.ac.uk",
    description = ("Harness for iRods cluster map/reduce analysis of newspaper corpus"),
    license = "MIT",
    keywords = "digital humanities research newspapers",
    url = "http://development.rc.ucl.ac.uk/",
    packages=['newsrods'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Research :: Humanities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
          'console_scripts': [
              'newsrods = newsrods.harness.query:main',
          ]
      },
)
