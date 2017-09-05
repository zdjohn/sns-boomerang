
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "sns_boomerang",
    version = "1.0.0",
    author = "John Di Zhang",
    author_email = "zhangdijohn@gmail.com",
    description = ("a serverless setup for scheduled tasks"),
    license = "MIT",
    keywords = "scheduled sns_resource",
    url = "http://packages.python.org/an_example_pypi_project",
    #    packages=['an_example_pypi_project', 'tests'],
    # long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
