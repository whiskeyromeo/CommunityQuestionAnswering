#!/usr/bin/env python

# Expects a stream of words on stdin, one word per line
# Emits a table of word counts and total word count

import sys

counts = {}
countSum = 0

for line in sys.stdin:
    line = line.strip()
    if line not in counts:
        counts[line] = 0
    counts[line] += 1
    countSum += 1

for word in counts.keys():
    print(counts[word], word)

print("Total:", countSum)
