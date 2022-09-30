#!/usr/bin/env python3
# Used with the dumped webpage contents of Spotify in order
#  to extract each song name and artist from the horrible
#  HTML that Spotify gives you.

import re

ex = re.compile(r'aria-label="Play ([^"]*) by ([^"]*)"')

seen = set()
i = 0
with open('songs') as f:
    for match in ex.findall(f.read()):
        if match[0] in seen:
            continue
        seen.add(match[0])
        i += 1
        print(f'{i}:  {match[0]} by {match[1]}')

