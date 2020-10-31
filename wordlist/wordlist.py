"""A library for the easy generation of lists of words from known sources
   for testing purposes"""

import bz2
import random
import re
import string
from typing import List, Dict, Callable, Tuple, Any


def _parse_words(seq: List[str], line: str) -> None:
    """if line is all lowercase add it to seq."""
    if all(c in string.ascii_lowercase for c in line):
        seq.append(line)


def _parse_wonderland(seq: List[str], line: str) -> None:
    """remove punctuation from line and add its words to seq."""
    line = line.strip()
    # if punctuation occurs within a word, kill it, outside a word space it
    # a string of puntuation suitably quoted for a regexp
    _punct_re = "[" + re.escape(string.punctuation) + "]+"

    # cpython caches the most recent compiled regexps so
    # this isn't as inefficient as it seems
    line = re.sub(r"(\w)%s(\w)" % _punct_re, r"\1\2", line)
    line = re.sub(r"[\s\b]%s" % _punct_re, " ", line)
    line = re.sub(r"%s[\s\b]" % _punct_re, " ", line)
    line = re.sub(r"(^%s)|(%s$)" % (_punct_re, _punct_re), " ", line)
    seq.extend(line.lower().split())


def _parse_surnames(seq: List[str], line: str) -> None:
    """add lowercased first element of line to self"""
    seq.append(line.split()[0].lower())


ListParser = Tuple[str, Callable[[List[str], str], None]]

_SOURCES: Dict[str, ListParser] = {
    # shortname: (data-file, parsing-function)
    "words": ("/usr/share/dict/words", _parse_words),
    "google10000": ("../wordlist/worddata/google-10000-english.txt", _parse_words),
    "surnames": ("./worddata/us1990.surnames.raw.bz2", _parse_surnames),
    "wonderland": ("./worddata/wonderland.txt.bz2", _parse_wonderland),
}

# standard small listing of frequently used "uninteresting" words
# TODO: do these want to be used or not?
_STOP_WORDS: List[
    str
] = """a able about across after all almost also am among an
    and any are as at be because been but by can cannot could
    dear did do does either else ever every for from get got
    had has have he her hers him his how however i if in into
    is it its just least let like likely may me might most
    must my neither no nor not of off often on only or other
    our own rather said say says she should since so some than
    that the their them then there these they this tis to too
    twas us wants was we were what when where which while who
    whom why will with would yet you your""".split()


class WordList(List[str]):
    """a list of lowercase, unpunctuated words from a known source"""

    def _load_source(self, source: str) -> None:
        """read a worlist from a named, known database"""
        filename, parser = _SOURCES[source]

        # we can handle compressed sources
        if filename.endswith(".bz2"):
            openf: Any = bz2.BZ2File
        else:
            openf = open

        def data_file_name(name):
            """return a path relative to this running script."""
            import os.path

            root = os.path.abspath(os.path.dirname(__file__))
            return os.path.join(root, name)

        # open the file decompressing as needed, call the specific parser
        with openf(data_file_name(filename)) as infile:
            for line in infile:
                sline: str = str(line).rstrip()
                if not sline:
                    continue
                parser(self, sline)

    def __init__(self, source: str = "words"):
        """create a wordlist from a predefined source"""
        # use a private RNG because this is a module and we don't want
        # to muck with the global RNG which may be in use
        super(WordList, self).__init__()
        self._myrand: random.Random = random.Random()
        self.source: str = source

        self._load_source(source)

    def shuffle(self) -> None:
        """Shuffles the wordlist in place.
        note: the total number of permutations of the list is likely larger
        than the period of the random number generators; this implies
        that most permutations can never be generated.

        This is a convenience function.
        """
        self._myrand.shuffle(self)

    def _partition(self, partitions: int) -> List[List[str]]:
        """Return a list containing partitions disjoint subsets of wordlist.
        Will destory random elements of the self to ensure
        equal length subsets are returned.

        If the list does not evenly divide into partitions, excess elements
        at the end will be dropped.
        """
        psize = len(self) // partitions
        parts = []
        for i in range(0, len(self), psize):
            parts.append(self[i : i + psize])
        return parts

    def dict(self) -> Dict[str, str]:
        """Return a dictionary made of pairings of the list."""
        key, value = self._partition(2)
        return dict(zip(key, value))
