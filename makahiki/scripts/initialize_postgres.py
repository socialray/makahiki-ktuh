#!/usr/bin/python

"""Invocation: scripts/initialize_postgres.py

Creates makahiki database and user within postgres database.
Assumes that the user postgres is trusted and can login without authentication.
This is usually the case by default.
"""

import sys
import urlparse
import os


def main():
    """main"""

    # get the db user password from DATABASE_URL environment variable
    if 'MAKAHIKI_DATABASE_URL' in os.environ:
        urlparse.uses_netloc.append('postgres')
        url = urlparse.urlparse(os.environ['MAKAHIKI_DATABASE_URL'])
        password = url.password
    else:
        print "Environment variable DATABASE_URL not defined. Exiting."
        sys.exit(1)

    if not password:
        print "password not in the Environment variable DATABASE_URL. Exiting."
        sys.exit(1)

    sqls = ("DROP DATABASE makahiki",
            "DROP USER makahiki; CREATE USER makahiki with CREATEDB PASSWORD '%s'" % password,
            "CREATE DATABASE makahiki OWNER makahiki",)

    for sql in sqls:
        command = 'psql -U postgres -c "%s"' % sql
        os.system(command)


if __name__ == '__main__':
    main()
