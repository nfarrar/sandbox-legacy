#!/usr/bin/env python

import re

# ipaddress hostname aliases
hf = open('/etc/hosts', 'r').readlines()

for line in hf:
  if not re.match('#|^\n', line):
    line = re.sub(r'\s+', ' ', line).expandtabs(1).strip()
    parts = line.split(' ')
    print parts
  else:
    print line.strip()
