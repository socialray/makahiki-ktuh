#!/usr/bin/python

"""Invocation: scripts/verify.py

Runs pep8, pylint, and tests.
If all are successful, there is no output and program terminates normally.
If any errors, prints output from unsuccessful programs and exits with non-zero error code.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir + os.sep)
from apps.utils import script_utils


def main(argv):
    """Verify main function. Usage: verify.py [-v | --verbose]"""

    current_dir = os.getcwd()
    manage_dir = script_utils.manage_py_dir()
    manage_py = script_utils.manage_py_command()

    verbose = script_utils.has_verbose_flag(argv)

    if verbose:
        print "running pep8"
    pep8_command = os.path.join("scripts", "run_pep8.sh")
    status = os.system("cd " + manage_dir + "; " + pep8_command)
    if status:
        sys.exit(1)

    if verbose:
        print "running pylint"
    pylint_command = os.path.join("scripts", "run_pylint.sh")
    status = os.system("cd " + manage_dir + "; " + pylint_command)
    if status:
        sys.exit(1)

    if verbose:
        print "cleaning"
    os.system("python " + manage_py + " clean_pyc")

    if verbose:
        print "running tests"
    status = os.system("python " + manage_py + " test")
    if status:
        sys.exit(1)

    if verbose:
        print "building docs"
    status = os.system("cd " + manage_dir + "; " + "cd ../doc; make clean html; cd " + current_dir)
    if status:
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
