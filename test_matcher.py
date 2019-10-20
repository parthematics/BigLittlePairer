from pair import Pairer

''' Our main script. It parses the given text files detailing each person's preferences
    and constructs the dictionaries needed to run our predefined methods. Outputs to STDOUT. '''

littles = dict((l, prefs.split(', ')) for [l, prefs] in (line.rstrip().split(': ') for line in open('littles.txt')))
bigs = dict((b, prefs.split(', ')) for [b, prefs] in (line.rstrip().split(': ') for line in open('bigs.txt')))
paired = Pairer(littles, bigs)
pairings = paired.pair()

for key in pairings.keys():
    print(key[0:1].upper() + key[1:] + ': ' + pairings[key][0:1].upper() + pairings[key][1:])
