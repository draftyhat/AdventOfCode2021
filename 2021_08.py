import sys;
import logging;

AOC_DAY=8
AOC_YEAR=2021

'''
7 segs  8
6 segs  0, 6, 9
            missing segment in 6 is a segment in 1 or 7
            missing segment in 0 is a segment in 4 but not 1
            missing segment in 9 is not a segment in 1,4,or 7
5 segs  2, 3, 5
            both missing segments in 2 are in 4
            only one missing segment in 5 is in 4
            both missing segments in 3 are not in 1 or 7
4 segs  4
3 segs  7
2 segs  1
'''

def decode_digits(samples, digits, logger):
    # return 4-digit encoded number

    # find 1, 4 in the samples
    one = ''
    four = ''
    for elt in samples.split():
        l = len(elt);
        if(2 == l):
            one = elt;
        elif(4 == l):
            four = elt;

    answer = 0;
    def found(digit):
        nonlocal answer
        answer = 10 * answer + digit;

    # decode the digits
    for elt in digits.split():
        if(2 == len(elt)):
            found(1);
        elif(3 == len(elt)):
            found(7);
        elif(4 == len(elt)):
            found(4);
        elif(5 == len(elt)):
            # found 2, 3, or 5
            # both missing segments in 2 are in 4
            # only one missing segment in 5 is in 4
            # both missing segments in 3 are not in 1 or 7

            # how many segments in this are also in 1?
            shares_with_one = 0;
            for seg in one:
                if(seg in elt):
                    shares_with_one += 1;
            if(2 == shares_with_one):
                found(3);
            else:
                shares_with_four = 0;
                for seg in four:
                    if(seg in elt):
                        shares_with_four += 1;
                logger.debug('{} shares {} segments with 4 ({})'.format(elt, shares_with_four, four));
                if(3 == shares_with_four):
                    found(5);
                else:
                    found(2);
        elif(6 == len(elt)):
            # found 0, 6, or 9
            # missing segment in 0 is a segment in 4 but not 1
            # missing segment in 6 is a segment in 1 or 7
            # missing segment in 9 is not a segment in 1,4,or 7

            # how many segments in this are also in 1?
            shares_with_one = 0;
            for seg in one:
                if(seg in elt):
                    shares_with_one += 1;
            if(2 == shares_with_one):
                # found 0 or 9
                shares_with_four = 0;
                for seg in four:
                    if(seg in elt):
                        shares_with_four += 1;
                if(3 == shares_with_four):
                    found(0);
                else:
                    found(9);
            else:
                found(6);
        elif(7 == len(elt)):
            found(8);

    logger.debug("Returning answer {}".format(answer));
    return answer;

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
    sum = 0;
    line = sys.stdin.readline();
    while(len(line) > 0):
        (samples, digits) = line.split('|');
        tally += tally_unique(line.split('|')[1]);
        sum += decode_digits(samples, digits, logger);
        line = sys.stdin.readline();

    print("Tally: {}".format(tally));
    print("Sum: {}".format(sum));


