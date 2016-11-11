#!/usr/bin/python3

"""Create a passphase in the style of xkcd 'correct horse battery staple'"""

from __future__ import print_function

import sys
import random

import wordlist


def correct_horse_battery_staple(words, word_count):
    """Return n cryptographically "strong" shorter words from the standard list
    without repeats as suggested in https://xkcd.com/936/
    """
    passphrase = []
    # use the system entropy generator, usually /dev/random
    sys_rand = random.SystemRandom()
    for _ in range(word_count):
        word = sys_rand.choice(words)
        words.remove(word)
        passphrase.append(word)
    return passphrase


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} n'.format(sys.argv[0]), file=sys.stderr)
        print('   where n is the number of cryptographically secure',
              file=sys.stderr)
        print('   choices from the wordlist. '
              'Use small n unless you are very patient.',
              file=sys.stderr)
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print('usage: {} n'.format(sys.argv[0]), file=sys.stderr)
        print('    n must be an integer', file=sys.stderr)
        sys.exit(1)

    words = wordlist.WordList('google10000')
    # limiting length of words from the list drops most stop words
    # and eliminates "sesquipedelian" at the cost of having the wordlist
    words = [x for x in words if 4 <= len(x) <= 7]
    print('dictionary size = {}'.format(len(words)))
    print(' '.join(correct_horse_battery_staple(words, n)))
