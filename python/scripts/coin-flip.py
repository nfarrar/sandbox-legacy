#!/usr/bin/env python

import random

def main():
    """ Using the random library, roll sequences of 4 boolean values.
        Record the rate of matching boolean sequences.  When a matching boolean
        sequence occurs, roll a fifth boolean value.  If the fifth boolean
        value is dissimilar to the boolean sequence, record an accurate
        prediction. """
    num_sims = 100000
    sequences = 0
    predictions = 0

    for sim in range(0, num_sims):
        coins = []
        for x in range(0,4):
            coins.append(random.randint(0,1))

        if coins[0] == coins[1] == coins[2] == coins[3]:
            sequences = sequences + 1
            guess = random.randint(0,1)
            if guess != coins[0]:
                predictions = predictions + 1

    print "Total Number of Simulations: " + str(num_sims)
    print "Number of Sequences: " + str(sequences)
    print "Number of Accurate Guesses: " + str(predictions)
    print "Frequency of Sequences: %.2f" % (float(sequences) / float(num_sims))
    print "Probability of Accurrate Guess: %.2f" % (float(predictions) / float(sequences))

if __name__ == "__main__":
    main()
