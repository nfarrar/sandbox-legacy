#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:             Nathan Farrar
# @Date:               2014-10-14 11:28:09
# @Last Modified by:   Nathan Farrar
# @Last Modified time: 2014-10-15 09:41:46


"""
    This LogParser is intended to work with any type of 'network flow' logs:

      - Proxy Logs
      - IDS Logs
      - HIPS Logs
      - Firewall Logs
      - etc

    Extremely dirty ATM. Lots of hard-coded junk, breaks easily.

    It probably makes sense to break LogParser into at least two separate
    classes, one for working with records, and one for reading the log
    files.

    The way CSVParser is written atm is bound heavily to the field names
    in the log files I'm parsing. This needs to be generalized.

    To make it work with many different types of CSV files (and files in
    general), it probably makes sense to build a generic LogReader object
    that can be subclassed.

    It also makes sense to move the backend storage to an in-memory Sqlite
    database, rather than listDiccts, to make queries much more
    straight-forward and extensible.

    TODO:
      - Unbind the field names from the methods & properties.
      - Add @wrapper for profiling executing times.
      - Colorize logging output when written to terminal.
      - Add command line interface. (CLIFF?)
      - Add web front end for browsing records?
      - Use tabulate to build ascii tables from listDicts?
      - Use gnuplot/gnuplot.py to build ascii graphs from listDicts? Matplotlib?
      - Need to learn pandas for better statistical analysis.
"""

import csv
import logging
import json
import os
import random
import re
import sys
from collections import Counter
from datetime import datetime
from pprint import pprint
from tabulate import tabulate
from urlparse import urlparse

import logging.config


class LogParser:
    """ Parse log records from a CSV file. """

    def __init__(self, name='Log Parser', pkl=None, csv=None, json=None, logger=None):
        """ Take a path. Identify the dialect and field names from the
        first row. """
        self.name = name
        self.logger = logger or logging.getLogger(__name__)

        self.logger.debug("Created new LogParser: '" + name + "'.")

        # Normalized data objects.
        self.fields = None
        self.records = []

        # Cached values, from @property methods.
        self.num_records = None
        self.first_record_datetime = None
        self.last_record_datetime = None

        if pkl != None:
            self.load_pkl(pkl)
        elif csv != None:
            self.load_csv(csv)
        elif json != None:
            self.load_json

    @property
    def record_count(self):
        if self.num_records == None:
            self.num_records = len(self.records)
        return self.num_records

    @property
    def first_timestamp(self):
        if self.first_record_datetime == None:
            for row in self.records:
                dt = row['datetime']
                if self.first_record_datetime == None or dt < self.first_record_datetime:
                    self.first_record_datetime = dt
        return self.first_record_datetime

    @property
    def last_timestamp(self):
        if self.last_record_datetime == None:
            for row in self.records:
                dt = row['datetime']
                if self.last_record_datetime == None or dt > self.last_record_datetime:
                    self.last_record_datetime = dt
        return self.last_record_datetime

    @property
    def duration(self):
        return self.last_record_datetime - self.first_record_datetime

    @property
    def domain_count(self):
        return len(self.counter('url_netloc'))

    @property
    def ip_count(self):
        return len(self.counter('client_ip'))

    @property
    def ua_count(self):
        return len(self.counter('user_agent'))

    def load_pkl(self, filename="data/records.pkl"):
        """ Load records from a pickle file. """
        self.logger.debug("Loading data from a pickle file is not yet supported.")
        sys.exit(1)

    def load_csv(self, filename="data/records.csv"):
        """ Parse log records from a CSV file. """

        try:
            csvfile = open(filename, 'rU')
            self.logger.debug('Opened ' + filename + " for reading.")
        except Exception, e:
            self.logger.error("Failed to open " + filename + " for reading.", exc_info=True)
            sys.exit(1)

        # Identify the csv dialect when opening the file.
        # self.dialect = csv.Sniffer().sniff(csvfile.read(1024))
        # csvfile.seek(0)

        # CSV dialect detection the Sniffer failed, hardcoding the
        # dialect for now.
        dialect = csv.excel

        # Parse the fields out and normalize their names. Make everything
        # lowercase and replace spaces with underscores.
        try:
            self.fields = next(csvfile).rstrip().lower().replace(" ", "_").split(',')
            csvfile.seek(0)
            self.logger.debug("Successfully parsed csv fields from header row.")
        except Exception, e:
            self.logger.error("An error occurred while parsing fields from header row.", exc_info=True)
            sys.exit(1)

        # Read the CSV as a dictionary, using the field mappings.
        try:
            csv_reader = csv.DictReader(csvfile, fieldnames=self.fields, dialect=dialect)
            self.logger.debug("Created csv.DictReader using parsed fields from header.")
        except Exception, e:
            self.logger.error("An error occurred while attempting to create csv.DictReader.", exc_info=True)
            sys.exit(1)

        # Skip the header row.
        try:
            n = next(csv_reader)
            self.logger.debug("Moved cursor to second row.")
        except Exception, e:
            self.logger.error("Failed to move cursor to second row.", exc_info=True)
            sys.exit(1)

        # Iterate over the rows in the csv.
        record_count = 0
        for row in csv_reader:

            # Parse the time string field into a datetime object and insert it
            # as a new field.
            try:
                row['datetime'] = LogParser.strtime_to_datetime(row['date_and_time'])
            except Exception, e:
                self.logger.error("Failed to parse datetime in " + filename + " on line " + str(record_count + 1) + ".", exc_info=True)
                sys.exit(1)

            # Use urlparse to split the url into parts and insert the them as new fields.
            # TODO: This needs to be abstracted to work with other CSV formats.
            try:
                urlparts = list(urlparse(row['url']))
                row['url_scheme'] = urlparts[0]
                row['url_netloc'] = urlparts[1]
                row['url_path'] = urlparts[2]
                row['url_params'] = urlparts[3]
                row['url_query'] = urlparts[4]
                row['url_fragment'] = urlparts[5]
            except Exception, e:
                self.logger.error("Failed to parse url in " + filename + " on line " + str(record_count + 1) + ".", exc_info=True)
                sys.exit(1)

            # Parse the extension from the path and insert it into a new field.
            try:
                row['url_ext'] = os.path.splitext(row['url_path'])[1][1:]
                self.records.append(row)
            except Exception, e:
                self.logger.error("Failed to parse url extension in " + filename + " on line " + str(record_count + 1) + ".", exc_info=True)
                sys.exit(1)

            record_count += 1

        # Report statistics upon successful completion.
        self.logger.info("Imported " + str(record_count) + " records from " + filename + ".")
        csvfile.close()

        # Append the custom field labels to the fields list.
        self.fields.append('datetime')
        self.fields.append('url_scheme')
        self.fields.append('url_netloc')
        self.fields.append('url_path')
        self.fields.append('url_params')
        self.fields.append('url_query')
        self.fields.append('url_fragment')
        self.fields.append('url_ext')

    def load_json(self, filename="data/records.json"):
        """ Load records from a json file. """
        self.logger.debug("Loading data from a json file is not yet supported.")
        sys.exit(1)

    def load_sqlite(self, filename="data/sqlite.csv"):
        """ Load records from a sqlite database. """
        self.logger.debug("Loading data from a sqlite database is not yet supported.")
        sys.exit(1)

    def save_pkl(self, filename="out/records.pkl"):
        """ Save records to a pickle file. """
        self.logger.debug("Saving data to a pickle file is not yet supported.")
        sys.exit(1)

    def save_csv(self, filename="out/records.csv"):
        """ Write records to csv file. """
        self.logger.debug("Saving data to a csv file is not yet supported.")
        sys.exit(1)

    def save_json(self, filename="out/records.csv"):
        """ Write records to json file. """
        try:
            jsonfile = (filename, 'w')
            json.dump(self.records, outfile, default=LogParser.datetime_to_strtime)
        except Exception, e:
            self.logger.error("Failed to open " + filename + " for writing.", exc_info=True)
        else:
            self.logger.info("Saved " + str(self.record_count) + " records to " + filename + ".")
            jsonfile.close()

    def save_sqlite(self, filename="out/sqlite.csv"):
        """ Save records to a SQLite database. """
        self.logger.debug("Saving data to a sqlite database is not yet supported.")
        sys.exit(1)

    def counter(self, field):
        """ Return a Counter containing the sum of unique elements in a
        specific field. """
        counter = Counter()
        for item in [record[field] for record in self.records]:
            counter[item] += 1
        return dict(counter)

    def sample(self, num=10):
        """ Return a random sample subset of records. """
        return random.sample(self.records, num)

    def search(self, field, pattern):
        """ Return a subset of records where pattern is found within
        the specified field. """
        records = []
        pattern = re.compile(pattern)

        for record in self.records:
            if re.search(pattern, record[field]) != None:
                records.append(record)
        return records

    def summary(self):
        """ Display information about the csv file.
        TODO: Abstract the unique counts.
        """
        summary_data = {
            'Record Count':                 self.record_count,
            'First Record':                 self.first_timestamp,
            'Last Record':                  self.last_timestamp,
            'Log Duration':                 self.duration,
            'Unique Domains':               self.domain_count,
            'Unique Clients':               self.ip_count,
            'Unique User Agent Strings':    self.ua_count
            }

        print ''.join([' ', self.name, ' ']).center(80, '-')

        for k, v in summary_data.items():
            print str(k).ljust(80 - len(str(v))) + str(v)

        print '-' * 80

    @staticmethod
    def line_count(filepath):
        """ Return the number of lines in a file. This is helpful for
        identifying if all records were imported, when lines and records have
        a 1-1 mapping. """

        try:
            f = open(filename)
            num_lines = sum(1 for line in f)
        except:
            print "The file " + filename + " could not be opened."
        finally:
            f.close()

        return num_lines

    @staticmethod
    def strtime_to_datetime(strtime):
        """ Return the datetime string as a native object.
        NOTE: The UTC offset is in a strange format. I'm preparsing it into
        the standard representation (superhack).
        """

        # Capture '+1:00' at end of time string.
        pattern = r"([\+|\-])(\d+):(\d\d)$"
        m = re.match(r".*" + pattern, strtime)

        # If we found a match, then rebuild the offset, using:
        # +0100' as the format. Replace the original occurrence.
        if m != None:
            offset = list(m.groups())
            offset[1] = offset[1].zfill(2)
            offset = ''.join(str(part) for part in offset)
            strtime = re.sub(r"([\+|\-])(\d+):(\d\d)$", "", strtime)

        # There's a bug in strptime ... docs say %z is supported, but it's
        # not. For now I'm discarding the offset.
        return datetime.strptime(strtime, '%d %b %Y %H:%M:%S %Z')

    @staticmethod
    def datetime_to_strtime(dto):
        """ Converts a datetime object back to a string, specifically for
        dumping the data to a json file."""

if __name__ == '__main__':

    # Read logging configuration & initialize logger.
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger(__name__)

    # Our default records file.
    csvfile = 'data/records.csv'

    # Create our parser, import records from a CSV, and display a summary.
    parser = LogParser(csv=csvfile)
    parser.summary()

    # Print the list of fields.
    print parser.fields

    # Extract and print a random sampling of records.
    # subset = parser.sample(2)
    # print subset

    # Get a counter containing the domains.
    domains = parser.counter('url_netloc')
    pprint(domains)

    # Get a list of the file extensions.
    exts = parser.counter('url_ext')
    pprint(exts)

    # Get a counter of the user-agent strings:
    uac = parser.counter('user_agent')
    pprint(uac)

    # Get a counter of the url paths:
    # for record in parser.search('url_query', 'exe'):
    #     print record['url']

    # Print a list of urls that accessed paths with a .dll extension.
    # for record in parser.search('url_ext', 'dll'):
    #     print record['url']

    # Print a counter of url schemes:
    # urlc = parser.counter('url_scheme')
    # pprint(cc)

    users = set()
    urls = set()
    ips = set()
    for record in parser.search('url_scheme', 'tcp'):
        users.add(record['user'])
        urls.add(record['url'])
        ips.add(record['client_ip'])

    print users, urls, ips
