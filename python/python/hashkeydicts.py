class HKObj:

    def __init__(self, name):
        self._name = name
        self._debug('__init__')

    def _debug(self, func):
        print self._name + '._debug: ' + func + '()'

    def __key__(self):
        self._debug('__key__')
        return self.__str__()

    def __hash__(self):
        self._debug('__hash__')
        return hash(self.__key__())

    def __repr__(self):
        self._debug('__repr__')
        return str(self.__hash__())

    def __str__(self):
        self._debug('__str__')
        return str(self._name)


d = {}

print '\n\n'
print 'creating hka ...'
hka = HKObj('hka')

print '\n'

print 'setting d[hka] = hka ... '
d[hka] = hka

print '\n'

print 'printing d ...'
print d, '\n'

print 'printing d[hka] ...'
print d[hka]

print hka.key
