from collections import defaultdict

class Pairer:
    def __init__(self, littles, bigs):

        self.L = littles
        self.B = bigs
        self.big2little = {}
        self.pairs = []

        self.little_rank = defaultdict(dict)
        self.big_rank = defaultdict(dict)

        for l, prefs in littles.items():
            for i, b in enumerate(prefs):
                self.little_rank[l][b] = i

        for b, prefs in bigs.items():
            for i, l in enumerate(prefs):
                self.big_rank[b][l] = i

    def prefers(self, b, l1, l2):
        return self.big_rank[b][l1] < self.big_rank[b][l2]

    def next_preference(self, l, b):
        ''' Return the big favored by l after b. '''

        i = self.little_rank[l][b] + 1
        return self.L[l][i]

    def pair(self, littles=None, next=None, big2little=None):
        ''' Try to match all littles with their preferred bigs. '''
        
        if littles is None:
            littles = self.L.keys()
        if next is None:
            next = dict((m, rank[0]) for m, rank in self.L.items())
        if big2little is None:
            big2little = {}
        if not len(littles):
            self.pairs = [(h, b) for b, h in big2little.items()]
            self.big2little = big2little
            return big2little
        l, littles = list(littles)[0], list(littles)[1:]
        b = next[l]
        next[l] = self.next_preference(l, b)
        if b in big2little:
            h = big2little[b]
            if self.prefers(b, l, h):
                littles.append(h)
                big2little[b] = l
            else:
                littles.append(l)
        else:
            big2little[b] = l
        return self.pair(littles, next, big2little)
