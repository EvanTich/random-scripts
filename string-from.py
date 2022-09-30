#!/usr/bin/python
# A quick and dirty way of stuffing a string into another, longer string.
#  Use it to hide hidden information or something...

import sys
import re

if len(sys.argv) < 3:
    print('Usage: string-from.py file strings...')
    sys.exit(1)

file = sys.argv[1]
strings = sys.argv[2:]

full_text = ''
with open(file) as f:
    full_text = re.sub('[\r\n]', '', f.read())

def silly_search(s, text, start=0):
    if not s:
        return []
    s = s.lower()
    text = text.lower()
    loc = []
    for i in range(start, len(text)):
        if s[0] == text[i]:
            loc.append(i)
            s = s[1:]
            if not s:
                break

    if s:
        return False
    return loc

def print_section(text, index, size=10):
    print(f'{index} {text[index]}: ...{text[index-size:index]}|{text[index]}|{text[index+1:index+size+1]}...')

last = 7
for s in strings:
    s = re.sub(r'\s', '', s)
    while True:
        loc = silly_search(s, full_text, last)
        if loc:
            break
        last -= 10
        if last < 0:
            print('Not possible')
            break

    for l in loc:
        print_section(full_text, l)
    print('====')

    last = loc[len(loc) - 1]


