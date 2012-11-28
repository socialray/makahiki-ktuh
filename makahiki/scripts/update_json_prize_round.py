'''
Created on Nov 27, 2012

@author: cmoore
'''
import sys
import getopt
import json


def main(argv):
    """Builds a mapping of round_name to pk and then updates the
    prize json file to use the round pk instead of round_name."""
    try:
        _, file_names = getopt.getopt(argv, "v", ["verbose"])
        round_info = {}
        if len(file_names) != 2:
            usage()
            sys.exit(2)
        else:
            round_info = get_round_info(file_names[0])
            #print round_info
            prize_info = json.load(open(file_names[1], 'r'))
            #print prize_info
            updated_prizes = update_prizes(prizes=prize_info, rounds=round_info)
            print updated_prizes
            updated_file = open("updated-%s" % file_names[1], 'w')
            json.dump(updated_prizes, updated_file, indent=4)
            updated_file.flush()
#            round_lines = open(file_names[0], 'r').readlines()
#            for line in round_lines:
#                words = line.split()
#                if words[0] == "{":
#                    parse_round(round_lines=round_lines, round_info=round_info)
    except getopt.GetoptError:
        usage()
        sys.exit(2)


def get_round_info(file_name):
    """Builds the mapping between round name and pk for the RoundSettings objects."""
    round_info = {}
    round_data = json.load(open(file_name, 'r'))
    for r in round_data:
        pk = r['pk']
        name = r['fields']['name']
        round_info[name] = pk
    return round_info


def update_prizes(prizes, rounds):
    """Updates the prizes round_name with the correct round pk."""
    for prize in prizes:
        fields = prize['fields']
        fk = rounds[fields['round_name']]
        fields['round'] = fk
        del fields['round_name']
    return prizes


def usage():
    """Prints out the Usage message to standard out."""
    print "Usage: update_json_prize_round <round .json> <prize.json>"

if __name__ == '__main__':
    main(sys.argv[1:])
