from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="dota-oracle",
    version="1.1",
    author="Bao Vien Ngo",
    author_email="bao.ngo@confirmit.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baovien/dota-oracle",
    packages=["doracle"],
    install_requires=['flask', 'requests'],
)
