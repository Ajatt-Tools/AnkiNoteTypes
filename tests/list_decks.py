from antp.ankiconnect import invoke


def list_decks():
    decks = invoke('deckNames')
    print("List of decks:")
    for deck in decks:
        print(deck)


if __name__ == '__main__':
    list_decks()
