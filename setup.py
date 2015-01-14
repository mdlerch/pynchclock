import re
from setuptools import setup

setup(
    name = "pynchclock",
    packages = ["pynchclock"],
    entry_points = {
        "console_scripts": ['pynchclock = pynchclock.pynchclock:main']
        },
    version = 0.01,
    description = "A CLI time tracker",
    long_description = "A CLI time tracker",
    author = "Michael Lerch",
    author_email = "mdlerch@gmail.com",
    url = "http://www.github.com/mdlerch/pynchclock",
    )
