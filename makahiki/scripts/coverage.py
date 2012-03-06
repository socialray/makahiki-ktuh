#!/usr/bin/python

"""Invocation:  scripts/coverage.py

Runs the tests and computes their coverage. An HTML coverage report is generated in htmlcov/."""

import os


def main():
    os.system("coverage erase")
    os.system("python manage.py clean_pyc")
    os.system("coverage run --source=apps manage.py test")
    os.system("coverage html")

if __name__ == '__main__':
    main()
