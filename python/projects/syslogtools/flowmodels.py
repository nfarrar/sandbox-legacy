from ipaddr import IPv4Address
from random import randint, choice

import logging
import pickle


class Flow:
    """
        This is an extensible network flow object.  By default there are four
        key pieces of data, source, destination, destination port & protocol.

        You can add any additional fields to a flow that yo may need using
        indices, for example: flow['time'] = timestamp.

        By default, regardless of any additional information in the flow,
        comparison and sorting is done based on the _.cmp_order list.

        If you need to modify the comparison order or add additional unique
        information to the flow, then modify this list to match the respective
        dictioanry keys.

        __str__ is overloaded to display all internal datamembers in an
        organized format.

        __hash__ is overloaded to return a hash of fields listed in .cmp_order.
    """

    def __init__(self, source, destination, port, protocol):
        self._dict = {'source': IPv4Address(source),\
            'destination': IPv4Address(destination), 'port': port, 'protocol': protocol}
        self._cmp_order = ['source', 'destination', 'port', 'protocol']

    def __eq__(self, b):
        return self.__hash__() == b.__hash__()

    def __str__(self):
        s = ""
        for i in self._dict.values():
            s = s + str(i) + '\t'
        return s

    def __key__(self):
        s = ""
        for i in self._cmp_order:
            s = s + str(self._dict[i])
        return s

    def __hash__(self):
        return str(hash(self.__key__()))

    def __getitem__(self, index):
        try:
            return self._dict[key]
        except:
            return None

    def __setitem__(self, key, value):
        try:
            self._dict[key] = value
        except:
            pass

    @property
    def hash(self):
        return self.__hash__()

    @staticmethod
    def random():
        """
            Return a random, valid flow.
        """
        source = str(randint(1,255)) + '.' + str(randint(1,255)) + '.' +\
            str(randint(1,255)) + '.' + str(randint(1,255))

        destination = str(randint(1,255)) + '.' + str(randint(1,255)) + '.' +\
            str(randint(1,255)) + '.' + str(randint(1,255))

        port = randint(1,65536)
        protocol = choice([ 'tcp', 'udp', 'icmp' ])

        return Flow(source, destination, port, protocol)

class FlowList:
    """
        Requirements:
        Maintain a UNIQUE list of FLows in memory.
        Maintain references to all flows.
        Maintain counts of how many times we loaded each flow.
    """

    def __getitem__(self, hash):
        # return [ hash, reference, count ]
        try:
            return [ hash, self._flows[hash], self._counts[hash] ]
        except:
            return None

    def __init__(self):
        self._flows = {}    # a dictionary of flows, indexed by the hash
        self._counts = {}   # a dictionary of flow counts, indexed by the hash

    def __iter__(self):
        return self.forward()

    def __len__(self):
        return len(self._flows)

    def counts(self):
        return self._counts.values()

    def forward(self):
        for hash in self._flows.keys():
            yield self.__getitem__(hash)

    def hashes(self):
        return self._flows.keys()

    def insert(self, flow):
        if flow.hash not in self._flows.keys():
            self._flows[flow.hash] = flow
            self._counts[flow.hash] = 0

        self._counts[flow.hash] = self._counts[flow.hash] + 1

    def keys(self):
        return self._flows.keys()

    @staticmethod
    def random(size, jitter):
        """
            Returns a Counter container full of random flows.
        """
        fl = FlowList()
        for x in range(0, size):
            f = Flow.random()
            for y in range(0, randint(0, jitter)):
                fl.insert(f)
        return fl

    def refs(self):
        return self._flows.values()

    def total(self):
        sum = 0
        for x in self._hash_counts.values():
            sum = sum + x
        return sum

    def unique(self):
        return self.__len__()

    @staticmethod
    def load(path):
        try:
            f = open(path, 'r')
            fl = pickle.load(f)
            f.close()
            logging.info('loaded flowlist with ' + str(len(fl)) + ' flows from ' + path)
            return fl
        except:
            logging.warning('failed to load flowlist from ' + path)
            return None


    def save(self, path):
        try:
            f = open(path, 'w')
            pickle.dump(self, f)
            logging.info('saved flowlist with ' + str(len(self)) + ' flows to ' + path)
            f.close()
        except:
            logging.warning('saving to ' + path + ' failed')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    """

    fl1 = FlowList.random(25, 5)
    fl1.save('test.pk')
    fl2 = FlowList.load('test.pk')

    f1 = Flow('1.1.1.1', '2.2.2.2', 22, 'tcp')
    f2 = Flow('1.1.1.1', '2.2.2.2', 22, 'tcp')
    f3 = Flow('1.1.1.1', '2.2.2.2', 33, 'tcp')
    print f1
    print f2
    print f1 == f2
    print f1 == f3
    f1['gunk'] == 'gunk'
    print f1 == f2

    fl = FlowList.random(25, 5)

    print fl.hashes(), '\n\n'
    print fl.refs(), '\n\n'
    print fl.counts(), '\n\n'

    for f in fl:
        f[1]['gunk'] = 'gunk'
        f[1]['moregunk'] = 'moregunk!!111one!'
    for f in fl:
        print f[1]
    """
