#! /usr/bin/env python
from distutils.core import setup

setup(name="sparqldb",
    version="0.0.1",
    description="Triple store that emulates a SQL database",
    author="John C Barstow",
    author_email = "jbowtie@amathaine.com",
    packages = ["."],
)

# package as tgz using git-archive
# use CDBS to convert distutils-based code into deb
# upload deb to PPA
# create launchpad project?? Need to understand lp/git integration if any

