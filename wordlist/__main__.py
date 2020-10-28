from wordlist import wordlist

def main():
    """Print a wordlist to standard out."""
    words = wordlist.WordList("google10000")
    for word in words:
        print(word)

if __name__ == "__main__":
    main()
