import pytest

import wordlist


def test_default_list():
    s = wordlist.WordList()

    assert len(s) > 40000


def test_google_list():
    s = wordlist.WordList("google10000")

    assert len(s) > 8000
    assert "music" in s
    assert "subjective" in s
