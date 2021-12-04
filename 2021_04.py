import sys;

CARDSIZE=5

class bingocard:
    def __init__(self):
        global CARDSIZE;

        # the sum of all currently unmarked numbers
        self.sum_unmarked = 0;

        # for each column, the number of marked numbers
        self.columns[CARDSIZE] = 

        # read 5 lines from stdin and assemble the card
        # we hold: a dictionary indexed by number and returning the position of
        # the number as a tuple (x, y), where (0,0) is top left and numbers
        # increase
