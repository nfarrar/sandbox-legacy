#!/usr/bin/env python

import ConfigParser
import datetime
import magic
import os
import re
import time

# a priortized list of potential malicious code signatures
code_signatures = {
    'eval': 0,
    'exec': 0,
    'charat': 0,
    'tostring': 0,
    'shell_exec': 0,
    'python_eval': 0,
    'passthru': 0,
    'iframe': 1,
    'base64_decode': 1,
    'gzip': 1,
    'gzinflate': 1,
    'gzuncompress': 1,
    'preg_replace': 1,
    'strrev': 2,
    'phpinfo': 2,
    'fopen': 3,
    'fwrite': 3,
    'fclose': 3,
    'readfile': 3,
    'mkdir': 3,
    'chmod': 3,
    'popen': 3,
    'system': 4,
    'phpinfo': 4
    }

# list of known malware signitures
variant_signatures = {
    'is_bot': 0,
    'filesman': 0,
    'tressa': 0
    }

def get_mime_type(file_path):
    """ returns the mime-type of the file or None if it cannot be determined """
    m = magic.open(magic.MAGIC_MIME)
    m.load()
    t = m.file(file_path)
    return t


def get_file_list(path):
    """ recurisvely walks the root path, building a comprehensive index of all files
    and returns them as a list """
    file_list = []
    for root, dirs, files in os.walk(path):
        for f in files:
            file_list.append(root + f)
    return file_list

def get_file_object(file_path):
    """ takes the full path of a file and returns a dictionary containing the files
    path, extension, mime-type, size """
    file_object = {}
    file_object['path'] = file_path
    file_object['name'] = os.path.basename(file_path)
    file_object['extension'] = os.path.splitext(file_object['name'])[1]
    file_object['mime-type'] = get_mime_type(file_path)
    (file_object['mode'], file_object['ino'], file_object['dev'],
        file_object['nlink'], file_object['uid'], file_object['gid'],
        file_object['size'], file_object['atime'], file_object['mtime'],
        file_object['ctime']) = os.stat(file_path)
    return file_object

def scan_for_malware(file_object):
    """ takes file object 'dictionary', scans it for potentially malicious
    code signatures, updates the file_object and returns it """
    pass

if __name__ == '__main__':
    """ uses ConfigParser to read the path from the wpscan.ini file
    not very robust yet, will fix in the future """
    config = ConfigParser.RawConfigParser()
    config.read(__config__)
    path = config.get('main', 'path')
    print 'building list of files'
    files = get_file_list(path)
    print 'build list of ' + str(len(files)) + ' files.'
    print get_file_object(files[1])
