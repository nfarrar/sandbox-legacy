#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import random
import re
import urllib
import urllib2


USER_AGENT_STRINGS = [
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)"
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1"
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)"
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)"
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)"
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)"
    "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US) Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)"
    ]


def get_search_terms(file_name):
    with open(file_name) as f:
        return f.readlines()


def get_random_agentstring():
    return random.choice


def gscrape(search_term):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    for start in range(0,10):
        url = 'http://www.google.com/search?q=' + search_term
        page = opener.open(url)
        soup = BeautifulSoup(page)
    for cite in soup.findAll('cite'):
        print cite.text


def do_test():
    print gscrape('nathan.farrar')


def do_work():
    search_terms = get_search_terms('addresses.txt')
    results = {}
    for search_term in search_terms:
        results[search_term] = gscrape(search_term)

if __name__ == '__main__':
    do_test()

