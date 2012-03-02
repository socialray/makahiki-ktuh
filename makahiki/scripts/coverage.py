#!/usr/bin/python

"""Runs the tests using the coverage command. The HTML coverage report is automatically
generated and placed in htmlcov/. If you want the plaintext report, run 
"coverage report -m".
"""

import os


def main():
    os.system("coverage erase")
    os.system("python manage.py clean_pyc")
    os.system("coverage run --source=apps manage.py test")
    os.system("coverage html")

if __name__ == '__main__':
    main()
