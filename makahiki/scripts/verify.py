#!/usr/bin/python

"""Invocation: scripts/verify.py

Runs pep8, pylint, and tests.
If all are successful, there is no output and program terminates normally.
If any errors, prints output from unsuccessful programs and exits with non-zero error code.
"""

import sys
import commands
import os
import getopt


def main(argv):
    verbose = 0
    try:
        opts, args = getopt.getopt(argv, "v", ["verbose"])
    except getopt.GetoptError:
        print "Usage verify.py [-v | --verbose]"
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-v", "--verbose"):
            verbose = 1
        
    if verbose == 1:
        print "running pep8"
        
    pep8_command = os.path.join("scripts", "run_pep8.sh")
    if verbose == 1:
        print "running pylint"
        
    pylint_command = os.path.join("scripts", "run_pylint.sh")
    (pep8_status, pep8_output) = commands.getstatusoutput(pep8_command)
    (pylint_status, pylint_output) = commands.getstatusoutput(pylint_command)
    if verbose == 1:
        print "cleaning"
        
    commands.getstatusoutput("python manage.py clean_pyc")
    if verbose == 1:
        print "running tests"
        
    (tests_status, tests_output) = commands.getstatusoutput("python manage.py test")
    if pep8_status:
        print "PEP ERROR OUTPUT:"
        print(pep8_output)
    if pylint_status:
        print "PYLINT ERROR OUTPUT:"
        print(pylint_output)
    if tests_status:
        print "TEST ERROR OUTPUT:"
        print(tests_output)
    if pep8_status or pylint_status or tests_status:
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
