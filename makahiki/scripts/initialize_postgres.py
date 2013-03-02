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
        username = url.username
        password = url.password
        database = url.path[1:]
    else:
        print "Environment variable MAKAHIKI_DATABASE_URL not defined. Exiting."
        sys.exit(1)

    if username:
        if not password:
            print "password not in the Environment variable MAKAHIKI_DATABASE_URL. Exiting."
            sys.exit(1)

        sqls = ("DROP DATABASE %s" % database,
                "DROP USER %s" % username,
                "CREATE USER %s with CREATEDB PASSWORD '%s'" % (username, password),
                "CREATE DATABASE %s OWNER %s" % (database, username),)

        for sql in sqls:
            command = 'psql -U postgres -c "%s"' % sql
            os.system(command)


if __name__ == '__main__':
    main()
