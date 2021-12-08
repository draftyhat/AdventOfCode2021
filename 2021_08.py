import sys;
import logging;

AOC_DAY=8
AOC_YEAR=2021

def tally_unique(line):
    # return how many 1s, 4s, 7s, or 8s appear in this line
    tally = 0;
    for elt in line.split():
        l = len(elt);
        if(l in [2, 3, 4, 7]):
            tally += 1

    return tally;


if('__main__' == __name__):
    import argparse;

    # deal with command line arguments
    parser = argparse.ArgumentParser(
            description = 'Advent of Code {} day {} solution'.format(
                AOC_YEAR, AOC_DAY));
    logger = logging.Logger('AOC{}d{}'.format(AOC_YEAR, AOC_DAY));
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

    tally = 0;
    line = sys.stdin.readline();
    while(len(line) > 0):
        tally += tally_unique(line.split('|')[1]);
        line = sys.stdin.readline();

    print(tally)


