#!/usr/bin/env python

# Expects a standard input stream with raw text data
# Emits an output stream with one word per line

import sys

def sanitizeWord(word):
    word = word.strip()
    word = word.lower()
    output = ""
    allowed = "abcdefghijklmnopqrstuvwxyz"
    for c in word:
        if c in allowed:
            output += c
    return output

for line in sys.stdin:
    words = line.split(' ')
    for word in words:
        word = sanitizeWord(word)
        if len(word) >= 1:
            print(word)
