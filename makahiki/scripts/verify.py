#!/usr/bin/python

"""Runs pep8, pylint, and tests.
If all are successful, there is no output and program terminates normally.
If any errors, prints output from unsuccessful programs and exits with non-zero error code.
"""

import sys
import commands


def main():
    (pep8_status, pep8_output) = commands.getstatusoutput("scripts/run_pep8.sh")
    (pylint_status, pylint_output) = commands.getstatusoutput("scripts/run_pylint.sh")
    commands.getstatusoutput("python manage.py clean_pyc")
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
    main()
