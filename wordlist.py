#!/usr/bin/python
"""A library for the easy generation of lists of words from known sources
   for testing purposes"""

# TODO: should probably parse aribtrary file contents also

import random
import bz2
import re
import string

__all__ = ['Wordlist']


class Wordlist(list):
    """a list of lowercase, unpunctuated words from a known source"""

    _sources = {
        'words': '/usr/share/dict/words',
        'surnames': '/home/msw/lib/us1990.surnames.raw.bz2',
        'wonderland': '/home/msw/lib/wonderland.txt.bz2',
    }

    # standard small listing of frequently used "uninteresting" words
    stop_words = """a able about across after all almost also am among an
        and any are as at be because been but by can cannot could
        dear did do does either else ever every for from get got
        had has have he her hers him his how however i if in into
        is it its just least let like likely may me might most
        must my neither no nor not of off often on only or other
        our own rather said say says she should since so some than
        that the their them then there these they this tis to too
        twas us wants was we were what when where which while who
        whom why will with would yet you your""".split()


    def _parse_wonderland(self, line):
        """remove punctuation from line and add its words to self"""
        line = line.strip()
        # if punctuation occurs within a word, kill it, outside a word space it
        # TODO: this could be cleaner I'm sure
        # a string of puntuation suitably quoted for a regexp
        _punct_re = '[' + re.escape(string.punctuation) + ']+'

        line = re.sub(r'(\w)%s(\w)' % _punct_re, r'\1\2', line)
        line = re.sub(r'[\s\b]%s' % _punct_re, ' ', line)
        line = re.sub(r'%s[\s\b]' % _punct_re, ' ', line)
        line = re.sub(r'(^%s)|(%s$)' % (_punct_re, _punct_re), ' ', line)
        self.extend(line.lower().split())

    def _parse_words(self, line):
        """if line is all lowercase add it to my self"""
        # blank lines are thrown out by the caller so we needn't check
        if all(c in string.ascii_lowercase for c in line):
            self.append(line)

    def _parse_surnames(self, line):
        """add lowercased first element of line to self"""
        self.append(line.split()[0].lower())

    def _load_source(self, source):
        """read a worlist from a named, known database"""
        filename = Wordlist._sources[source]

        # we can handle compressed sources
        if filename.endswith('.bz2'):
            openf = bz2.BZ2File
        else:
            openf = open

        parsef = getattr(self, '_parse_' + source)

        # open the file decompressing as needed, call the specific parser
        with openf(filename) as infile:
            for line in infile:
                line = line.rstrip()
                if not line:
                    continue
                parsef(line)


    def __init__(self, source='words'):
        """create a wordlist from a predefined source"""
        # use a private RNG because this is a module and we don't want
        # to muck with the global RNG which may be in use
        super(Wordlist, self).__init__()
        self._myrand = random.Random()
        self.source = source

        self._load_source(source)

    def shuffle(self):
        """shuffles the wordlist in place
           note: the total number of permutations of the list is larger
           than the period of the random number generators; this implies
           that most permutations can never be generated."""
        self._myrand.shuffle(self)

    def partition(self, partitions):
        """returns a list containing partitions disjoint subsets
           will destory random elements of the self to ensure
           equal length subsets are returned"""
        # throw away random items to make len(self) a multiple of partitions
        while len(self) % partitions:
            kill = self._myrand.choice(self)
            self.remove(kill)

        psize = len(self)//partitions
        parts = []
        for i in range(0, len(self), psize):
            parts.append(self[i:i+psize])
        return parts

    def dict(self):
        """return a dictionary made of pairings of the wordlist"""
        key, value = self.partition(2) # pylint: disable=unbalanced-tuple-unpacking
        return dict(zip(key, value))
