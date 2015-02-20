#!/usr/bin/env python


from random import randint


class IterableListWrapper:
    def __init__(self):
        self._list = []
        for x in range(0, randint(10, 25)):
            self._list.append(randint(1, 65536))

    def __getitem__(self, index):
        return self._list[index]

    def __iter__(self):
        return self._forward()

    def __len__(self):
        return len(self._list)

    def _forward(self):
        current_item = 0
        while current_item < len(self._list):
            yield self._list[current_item]
            current_item = current_item + 1


class IterableDictWrapper:
    def __init__(self):
        self._dict = {}
        for x in range(0, randint(10, 25)):
            self._dict[str(randint(0, 65536))] = randint(0, 65535)

    def __iter__(self):
        return self._forward()

    def _forward(self):
        for v in self._dict.values():
            yield v


il = IterableListWrapper()
#for x in il:
#    print x
#for x in range(0, len(il)):
#    print x, il[x]

id = IterableDictWrapper()

for x in id:
    print x
