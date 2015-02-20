import dataimporter
import logging
import re


class LogParser:

    """
        This is a generic log parser.  A single log line is input, we search
        for an ip addresses and return a list of the results.
    """

    _regex = None
    _ip_address = r'((?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}))'

    def __init__(self, regex=None):
        if regex == None:
            self._regex = self._ip_address
        else:
            self._regex = regex

    def parse(self, line):
        result = re.search(self.regex, line)
        try:
            return result.groups()
        except:
            return None

    @property
    def regex(self):
        return self._regex

class ASASyslogParser(LogParser):

    _junk = r'.*?'
    _syslog_id = r'(106100)'
    _protocol = r'(tcp|udp)'
    _interface = r'(pci_inside|pci_outside|pci-npci_dmz)'
    _ip_address = r'((?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}))'
    _port = r'([\d]{1,5})'

    _asa_106100 = _junk + _syslog_id + _junk + _protocol + _junk +\
        _interface + r'//?' + _ip_address + r'\(' + _port + r'\).*?' +\
        _interface + r'//?' + _ip_address + r'\(' + _port + r'\)'

    def __init__(self):
        LogParser.__init__(self, self._asa_106100)


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    importer = dataimporter.ZipImporter("/home/oxseyn/Documents/hp_data/2011.08.11-2011.08.28/compressed_data/")
    subset = importer.subset(0,20)
    p = ASASyslogParser()
    for line in subset:
        print p.parse(line)


