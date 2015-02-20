import os
from setuptools import setup


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="nfarrar-sandbox",
    version="0.0.1",
    author="Nathan Farrar",
    author_email="nathan.farrar@gmail.com",
    description=("A project containing various 'learning' scripts."),
    license = "GNUv3",
    keywords = "nfarrar sandbox learning",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['an_example_pypi_project', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
