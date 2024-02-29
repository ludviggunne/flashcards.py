#! /usr/bin/env python3

import random, tomllib, sys, os, curses

class Flashcard:
    def __init__(self, q, a):
        self.q = q
        self.a = a

    def __str__(self):
        return f'Q: {self.q}, A: {self.a}'

class Deck:
    def __init__(self, source):
        data = tomllib.loads(source)
        cards = data['card']
        self.cards = []
        for card in cards:
            q = card['Q']
            a = card['A']
            self.cards.append(Flashcard(q, a))

    def __iter__(self):
        return self.cards.__iter__()

    def __len__(self):
        return self.cards.__len__()

    def shuffle(self):
        random.shuffle(self.cards)

def center(stdscr, string):
    y = int(curses.LINES / 2)
    x = int((curses.COLS - len(string)) / 2)
    stdscr.move(y, 0)
    stdscr.deleteln()
    stdscr.addstr(y, x, string)

def display(stdscr, string):
    center(stdscr, string)
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)

    filename = None
    if len(sys.argv) == 1:
        filename = 'flashcards.toml' # default filename
    else:
        filename = sys.argv[1]

    source = None

    with open(filename, 'r') as f:
        source = f.read()

    deck = None

    try:
        deck = Deck(source)
    except (KeyError, tomllib.TOMLDecodeError) as e:
        print(e)
        sys.exit('Invalid flashcards file')

    deck.shuffle()
    try:
        for i, card in enumerate(deck, start=1):
            y = int(curses.LINES / 2)
            qstr = f'Question {i}/{len(deck)}'
            x = int((curses.COLS - len(qstr)) / 2)
            stdscr.addstr(y - 2, x, qstr, curses.A_UNDERLINE)

            x = int((curses.COLS - len(card.q)) / 2)
            stdscr.addstr(y, x, card.q)
            stdscr.refresh()
            stdscr.getch()

            x = int((curses.COLS - len(card.a)) / 2)
            stdscr.addstr(y + 2, x, card.a)
            stdscr.refresh()
            stdscr.getch()

            stdscr.move(y + 2, 0)
            stdscr.deleteln()
            stdscr.move(y, 0)
            stdscr.deleteln()
    except:
        pass

if __name__ == "__main__":
    curses.wrapper(main)
