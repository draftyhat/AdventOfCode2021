import sys;
import logging;

AOC_DAY=4
CARDSIZE=5

class bingocard:
    def __init__(self, logger = None):
        global CARDSIZE;
        self.logger = logger;

        # the sum of all currently unmarked numbers
        self.sum_unmarked = 0;

        self.win = False;

        # for each column, row, and the two diagonals, the number of marked
        # numbers
        self.columns = [0] * CARDSIZE;
        self.rows = [0] * CARDSIZE;
        self.forward_diagonal = 0;
        self.backslash_diagonal = 0;

        # read 5 lines from stdin and assemble the card
        # we hold: a dictionary indexed by number and returning the position of
        # the number as a tuple (x, y), where (0,0) is top left and numbers
        # increase
        self.card = {}
        rown = 0;
        for rown in range(CARDSIZE):
            nextrow = sys.stdin.readline().split();
            for index, val in enumerate(nextrow):
                val = int(val)

                # for each number read in, store position on the card in our dict
                self.card[val] = (rown, index);

                # add to the unmarked sum
                self.sum_unmarked += val;

    def _check_win(self, nmarked):
        global CARDSIZE;

        # if CARDSIZE elements in this row, column, or diagonal, are marked,
        # bingo!
        if(nmarked == CARDSIZE):
            self.win = True;

    def mark(self, i):
        # mark this number
        # if it's on our card, get its position
        try:
            (x, y) = self.card[i];
            self.sum_unmarked -= i;
            # mark it on the column, row, and diagonal
            self.rows[x] += 1;
            self._check_win(self.rows[x]);
            self.columns[y] += 1;
            self._check_win(self.columns[y]);
            if(x == y):
                self.forward_diagonal += 1;
                self._check_win(self.forward_diagonal);
            elif(x + y == CARDSIZE - 1):
                self.backslash_diagonal += 1;
                self._check_win(self.backslash_diagonal);
        except:
            # number was not on this board
            pass;

    def won(self):
        return self.win;

    def get_sum_unmarked(self):
        # property
        return self.sum_unmarked;

    def __repr__(self):
        # yeah, because of our weird internal storage, printing out the board
        # is hard. We go through the dictionary, store all the numbers in the
        # human-intuitive manner, and then print them.
        # this is just for debugging. If we needed this representation for
        # real, it'd be good to store it upon input.

        # heh, this doesn't work. It copies the first row by reference CARDSIZE times.
        # displaycard = [[0] * CARDSIZE] * CARDSIZE
        displaycard = [];
        for i in range(CARDSIZE):
            displaycard.append([0] * CARDSIZE);

        for (val, (x, y)) in self.card.items():
            displaycard[x][y] = val;

        retval = '<';
        for row in displaycard:
            retval += ' '.join(['{:2d}'.format(elt) for elt in row]);
            retval += '\n ';
        retval += '  Column mark count: {}'.format(
            ' '.join(['{}'.format(x) for x in self.columns]));
        retval += '  Row mark count:    {}\n'.format(
            ' '.join(['{}'.format(x) for x in self.rows]));
        retval += '  Forward diagonal mark count: {}   Backslash diagonal' \
                ' mark count: {}\n'.format(
                    self.forward_diagonal, self.backslash_diagonal);
        retval += '  Unmarked sum: {}>'.format(self.sum_unmarked);
        return retval;


if('__main__' == __name__):
    import argparse;

    # deal with command line arguments
    parser = argparse.ArgumentParser(
            description = 'Advent of Code day {} solution'.format(AOC_DAY));
    logger = logging.Logger('AOCd{}'.format(AOC_DAY));
    logger.addHandler(logging.StreamHandler());

    parser.add_argument(
        '-2', '--part2', action='store_true',
        help='part 2?', default=False);
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='be verbose', default=False);

    args = parser.parse_args();
    if(args.verbose):
        logger.setLevel(logging.DEBUG);

    # read the drawn numbers
    drawn = sys.stdin.readline().split(',');
    # read the 3 bingo cards
    cards = [];
    # read a blank line, then read the next card
    while(sys.stdin.readline()):
        cards.append(bingocard());
        logger.debug("card {}:\n{}".format(len(cards), cards[-1]));

    # input drawn numbers to each card, check for win, get answer
    for drawnn in drawn:
        drawnn = int(drawnn);
        print("--- drawing {}".format(drawnn));
        for cardindex, card in enumerate(cards):
            card.mark(drawnn);
            if(card.won()):
                if(args.part2):
                    cards.pop(cardindex);
                    logger.debug("Card {} won with draw {}!".format(cardindex, drawnn));
                    if(len(cards) == 1):
                        logger.debug("Last card {} won with draw {}!".format(cardindex, drawnn));
                        logger.debug(card);
                        print(drawnn * card.sum_unmarked);
                        sys.exit(0);
                else:
                    logger.debug(card);
                    print(drawnn * card.sum_unmarked);
                    sys.exit(0);

