import logging
import os
import zipfile

class ZipImporter:
    def __init__(self, path):
        self._archives = []
        self._files = []
        self._lines = []

        self._num_archives = 0
        self._num_files = 0
        self._num_lines = 0

        try:
            for file in os.listdir(path):
                if zipfile.is_zipfile(path + file):
                    logging.debug('adding ' + path + file)
                    self._archives.append(zipfile.ZipFile(path + file))
                else:
                    logging.debug('ignoring' + path + file)
        except OSError:
            logging.debug('directory listing failed.')

    def __iter__(self):
        self._archive_index = 0
        self._file_index = 0
        self._line_index = 0
        self._files = []
        self._lines = []
        return self

    def __len__(self):
        return self._num_lines

    def next(self):
        # logging.debug('importer.next() : method entry point')
        # if a line is available return it and increment line counter
        #if self._line_index < len(self._lines) - 1:
        if self._line_index < len(self._lines):
            self._line_index = self._line_index + 1
            if self._line_index < len(self._lines): # to prevent an extra line
                self._num_lines = self._num_lines + 1
            return self._lines[self._line_index - 1]
        else:
            # logging.debug('importer.next() : no line to return')
            # if a line was not available
            # if a file is available, load it, increment file counter
            # reset line counter, and recurse
            if self._file_index < len(self._files):
                self._num_files = self._num_files + 1
                self._lines = self._archives[self._archive_index - 1].open(self._files[self._file_index - 1]).readlines()
                logging.debug('loaded ' + str(len(self._lines)) + ' lines.')
                self._file_index = self._file_index + 1
                self._line_index = 0
                return self.next()
            else:
                # if a file was not available
                # if an archive is available, load the files, reset the file counter,
                # increment archive counter, and recurse
                if self._archive_index < len(self._archives):
                    self._num_archives = self._num_archives + 1
                    logging.debug('loaded archive ' + str(self._archive_index + 1) + ' of ' + (str(len(self._archives))))
                    self._files = self._archives[self._archive_index].namelist()
                    self._file_index = 0
                    self._archive_index = self._archive_index + 1
                    return self.next()
                else:
                    # no more archives are available
                    raise StopIteration

    def subset(self, start, end):
        count = 0
        subset = []
        for line in self:
            if count < start:
                pass
            elif count >= start and count < end:
                subset.append(line)
            else:
                self._num_lines = self._num_lines - 1 # this will be 1 off in rare cases
                break
            count = count + 1
        return subset


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    path = "/home/oxseyn/Documents/hp_data/2011.07.03-2011.07.11/archives/"

    importer = ZipImporter(path)

    print 'first archive has 159882 lines'
    print ''
    print 'len(importer):\t', len(importer)
    print 'type(importer):\t', type(importer)
    print ''

    x = 0
    y = importer.subset(0,20)
    print 'len(y):\t\t', len(y)
    print 'type(y):\t', type(y)
    print ''

    print 'len(importer):\t', len(importer)
