"""Create a passphase in the style of xkcd 'correct horse battery staple'"""

import sys
import random

from . import wordlist


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


def main():
    if len(sys.argv) != 2:
        print("usage: {} n".format(sys.argv[0]), file=sys.stderr)
        print("   where n is the number of cryptographically secure", file=sys.stderr)
        print("   choices from the wordlist.", file=sys.stderr)
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("usage: {} n".format(sys.argv[0]), file=sys.stderr)
        print("    n must be an integer", file=sys.stderr)
        sys.exit(1)

    words = wordlist.WordList("words")
    # limiting length of words from the list drops most stop words
    # and eliminates "sesquipedelian" at the cost of having the wordlist
    words = [x for x in words if 4 <= len(x) <= 7]
    print(f"dictionary size = {len(words)}")
    print(" ".join(correct_horse_battery_staple(words, n)))


if __name__ == "__main__":
    main()
