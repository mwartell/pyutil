#!python3

import wordlist

w = wordlist.WordList('words')
tenth = w[10]

print(type(tenth))
tenth *= 5


print(w[:10])
