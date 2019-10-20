from collections import defaultdict

class Pairer:
    ''' Instantiating the Pairer class creates the data structures that will be necessary
    effectively run the Gale-Shapley Stable Marriage algorithm. The "littles" and "bigs"
    arguments are read in from their respective files ('littles.txt' and 'bigs.txt') and
    populated as dictionaries mapping each individual to a list of their preferences. '''
    def __init__(self, littles, bigs):

        self.L = littles
        self.B = bigs
        # big_to_little is a dictionary of potential mappings between each big and a corresponding little.
        # This dictionary will be continuously modified during the execution of the algorithm.
        self.big_to_little = {}
        # pairs is a list containing the FINAL pairings between each big and little. It will be outputted in __main__.
        self.pairs = []

        # NOTE: little_rank and big_rank are nested dictionaries that keep track of each little's
        # ranking for a given big in an easily accessible fashion (i.e. little_rank[l][b]),
        # and vice versa for bigs. This was the motivation behind using a defaultdict.
        self.little_rank = defaultdict(dict)
        self.big_rank = defaultdict(dict)

        # Populating our little_rank and big_rank dictionaries, as described above.
        for l, prefs in littles.items():
            for i, b in enumerate(prefs):
                self.little_rank[l][b] = i

        for b, prefs in bigs.items():
            for i, l in enumerate(prefs):
                self.big_rank[b][l] = i

    ''' Returns a boolean corresponding to whether big b prefers little l1 to little l2. '''
    def prefers(self, b, l1, l2):
        return self.big_rank[b][l1] < self.big_rank[b][l2]

    ''' Return the big favored by l after b. '''
    def next_preference(self, l, b):
        i = self.little_rank[l][b] + 1
        return self.L[l][i]

    ''' Main algorithm that matches all littles with their preferred bigs, in line with the
        original approach described by Gale and Shapley. '''
    def pair(self, littles=None, next=None, big_to_little=None):
        # Populating the main data structures used through the algorithm.
        if littles is None:
            littles = self.L.keys()
        # next is a dictionary mapping each little to their CURRENT favorite choice for big.
        # This is why the algorithm is little-optimal.
        if next is None:
            next = dict((m, rank[0]) for m, rank in self.L.items())
        if big_to_little is None:
            big_to_little = {}

        # Our terminating condition. Once there are no littles left, we know that our pairings are now optimal.
        # NOTE: This version of the algorithm is set up to be LITTLE OPTIMAL.
        if not len(littles):
            self.pairs = [(h, b) for b, h in big_to_little.items()]
            self.big_to_little = big_to_little
            return big_to_little

        l, littles = list(littles)[0], list(littles)[1:]
        b = next[l]
        # Here, we switch l's BEST option for big to be their next preferred option.
        next[l] = self.next_preference(l, b)

        # Switching preferences for bigs and littles. This is where the meat of the algorithm takes place.
        # We append the less preferred option for little to the end of the list so we can take care of them later.
        if b in big_to_little:
            h = big_to_little[b]
            if self.prefers(b, l, h):
                littles.append(h)
                big_to_little[b] = l
            else:
                littles.append(l)
        else:
            big_to_little[b] = l

        # Our recursive call. This is called to run the next iteration of stable marriage until every little is paired
        # with their best available option for big (i.e. there are no rogue pairs of bigs and littles).
        return self.pair(littles, next, big_to_little)
