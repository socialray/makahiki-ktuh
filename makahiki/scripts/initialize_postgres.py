#!/usr/bin/python

"""Creates makahiki database and user within postgres database.
Assumes that the user postgres is trusted and can login without authentication.
This is usually the case by default.
"""

import sys
import commands
import os


def main():
    sql_file = os.path.join("scripts", "initialize_postgres.sql")
    command = "psql -U postgres -f " + sql_file
    (initialize_status, initialize_output) = commands.getstatusoutput(command)
    print initialize_output
    sys.exit(initialize_status)

if __name__ == '__main__':
    main()
