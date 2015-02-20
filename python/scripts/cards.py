#!/usr/bin/env python
import random

def main():
    """  For num_sims simulations, randomly shuffle a deck of cards.
        Calculate the frequency of face cards in the front half of the deck
        and the frequency of face cards in the back of the deck.  Calculate the
        average rate of occurance of face cards in the front half vs. the
        back half of the deck.  """

    # I am ignoring suit in the deck, since for these calculations it does
    # not matter.

    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q,', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q,', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q,', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q,', 'K', 'A']

    num_sims = 10000
    front_total = 0
    back_total = 0

    for sim in range(0,num_sims):
        random.shuffle(deck)
        front = 0   # counts face cards in first 26 positions in the deck
        back = 0    # counts face cards in last 26 positions in the deck

        for x in range(0,52):
            if deck[x] in ['J', 'Q', 'K', 'A']:
                if x < 26:
                    front = front + 1
                else:
                    back = back + 1

        front_total = front_total + front
        back_total = back_total + back

    avg_front = float(front_total) / float(num_sims)
    avg_back = float(front_total) / float(num_sims)

    print "Number of simulations: %i" % (num_sims)
    print "Average number of face cards in front of deck: %.1f" % (avg_front)
    print "Average number of cards cards in back of deck: %.1f" % (avg_back)

if __name__ == "__main__":
    main()
