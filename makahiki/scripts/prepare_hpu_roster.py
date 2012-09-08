#!/usr/bin/python

"""
Invocation:  scripts/prepare_uh_roster.py infile outfile
"""

import csv
import sys


def main(args):
    """
    prepare the csv file from HPU roster
    """
    if len(args) != 2:
        print "usage: prepare_hpu_roster infile outfile."
        return

    try:
        infile = open(args[0])
        outfile = open(args[1], "wb")
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
    except IOError:
        print "Can not open file, Aborting.\n"
        return

    row = 0
    for items in reader:
        row += 1
        if row == 1:
            # skip the first row
            continue

        # roster format: row id,Last Name,First Name,Assigned Room,E-mail
        lastname = items[1].strip().capitalize()
        firstname = items[2].strip().capitalize()

        team = items[3].split("-")[0].strip().capitalize()
        if not team:
            print "==== ERROR ==== no team assign for user %s,%s" % (
                lastname, firstname)

        email = items[4].strip()
        if not email.endswith("@my.hpu.edu"):
            print "==== ERROR ==== non-hpu edu email: %s for user %s,%s" % (
                email, lastname, firstname)
            sys.exit(1)

        username = email.split("@")[0]

        # output format: team, firstname, lastname, email, username, password[, RA]
        writer.writerow([team, firstname, lastname, email, username, ''])
    infile.close()
    outfile.close()


if __name__ == '__main__':
    main(sys.argv[1:])
