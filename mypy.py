#!python3

from wordlist import WordList

a = list(range(5))
w = WordList('words')

print(type(w))
print(w[0].upper())
for i in w[10:20]:
    print(i)
