# use regexes, or string masking, to find winner boards
import sys;
import logging;

AOC_DAY=4
CARDSIZE=5

class bingocard:
    def __init__(self, logger = None):
        global CARDSIZE;
        self.logger = logger;
        self.markchar = '.';

        # read in the board as a string
        self.card = sys.stdin.read(CARDSIZE * CARDSIZE * 3);
        if(len(self.card) != CARDSIZE * CARDSIZE * 3):
            raise Exception("Badly formatted card! Card string" \
                    " is:\n{}".format(self.card));

    def mark(self, i):
        # mark this number, if it's in our card
        istring = '{:2d}'.format(i);
        for i in range(CARDSIZE * CARDSIZE):
            if(self.card[i*3:i*3 + 2] == istring):
                #self.card[i*3] = self.markchar;
                #self.card[i*3 + 1] = self.markchar;
                self.card = self.card[:i*3] \
                    + self.markchar * 2 + self.card[i*3 + 2:];
                return True;
        return False;

    def sum_unmarked(self):
        # sum unmarked numbers in this card
        sum = 0;
        for i in range(CARDSIZE * CARDSIZE):
            try:
                x = int(self.card[i*3:i*3+2]);
                sum += x;
            except:
                # wasn't an integer
                pass;
        return sum;

    def won(self):
        # painstakingly match each winning row, column, and NOT THE DIAGONALS
        # pattern to the actual card to see if we won rows
        for rown in range(CARDSIZE):
            rowstart = 1 + rown * CARDSIZE * 3;
            for colpos in range(CARDSIZE):
                if(self.card[rowstart + colpos * 3] != self.markchar):
                    # unmarked square. Abort.
                    break;
            else:
                # this row won!
                return True;

        # columns
        for columnn in range(CARDSIZE):
            columnstart = 1 + columnn * 3;
            for rown in range(CARDSIZE):
                if(self.card[columnstart + rown * CARDSIZE * 3] !=
                        self.markchar):
                    # unmarked square. Abort.
                    break;
            else:
                # this column won!
                return True;

        # forward diagonal
        #for xy in range(CARDSIZE):
        #    if(self.card[1 + xy * CARDSIZE * 3 + xy * 3] !=
        #                self.markchar):
        #            # unmarked square. Abort.
        #            break;
        #else:
        #    # this diagonal won!
        #    return True;

        # backward diagonal
        #for xy in range(CARDSIZE):
        #    if(self.card[1 + xy * CARDSIZE * 3 + (CARDSIZE - xy) * 3] !=
        #                self.markchar):
        #            # unmarked square. Abort.
        #            break;
        #else:
        #    # this diagonal won!
        #    return True;


    def __repr__(self):
        return self.card;



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
    logger.debug("---- starting play ----");

    # input drawn numbers to each card, check for win, get answer
    trackedcard = cards[1];
    for drawnn in drawn:
        drawnn = int(drawnn);
        topop = [];
        for cardindex, card in enumerate(cards):
            card.mark(drawnn);
            print("-- marking {}".format(drawnn));
            print(card);
            if(card.won()):
                if(args.part2):
                    logger.debug("Card {} won with draw {}!".format(cardindex, drawnn));
                    logger.debug(card);
                    if(len(cards) == 1):
                        logger.debug("Last card {} won with draw {}!".format(cardindex, drawnn));
                        print(drawnn * card.sum_unmarked());
                        sys.exit(0);
                    topop.insert(0, cardindex)
                else:
                    logger.debug(card);
                    print(drawnn * card.sum_unmarked());
                    sys.exit(0);
        for cardindex in topop:
            cards.pop(cardindex);


