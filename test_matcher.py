from pair import Pairer

littles = dict((l, prefs.split(', ')) for [l, prefs] in (line.rstrip().split(': ') for line in open('littles.txt')))

bigs = dict((b, prefs.split(', ')) for [b, prefs] in (line.rstrip().split(': ') for line in open('bigs.txt')))

paired = Pairer(littles, bigs)

pairings = paired.pair()

print(pairings)
