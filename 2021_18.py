import sys;
import logging;
import re;

AOC_DAY=14
AOC_YEAR=2021


pairherere = re.compile('^(\d+),(\d+)(.*)');
rightmostdigitre = re.compile('.*(\d+)([^\d]*)');
leftmostdigitre = re.compile('[^\d]*(\d+)(.*)');

def explode(snailfish, logger):
    # find the leftmost depth-4 pair and explode it.
    # work with the text representation of the number (no spaces)
    st = str(snailfish).replace(' ','');
    depth = 0;
    last_number_index = None;
    for index, item in enumerate(st):
        if '[' == item:
            depth += 1;
        elif ']' == item:
            depth -= 1;
        elif depth >= 4:
            logger.debug(f'explode: depth 4 at {index} "{st[index:]}"');
            # find out if there's a pair here
            match = pairherere.match(st[index:]);
            if(match):
                logger.debug(f"explode: found pair at {index}"); 
                # explode this pair
                stfirsthalf = st[:index-1];
                stlasthalf = st[index + match.start(3)+1:];
                # new string will be firsthalf 0 lasthalf
                # add first in matched pair to rightmost digit preceding match
                rightmostdigit_match = rightmostdigitre.match(stfirsthalf);
                if(rightmostdigit_match):
                    stfirsthalf = stfirsthalf[:rightmostdigit_match.start(1)] + \
                            str(int(match.group(1)) + int(rightmostdigit_match.group(1))) + \
                            stfirsthalf[rightmostdigit_match.start(2)];

                # add last in matched pair to leftmost digit following match
                leftmostdigit_match = leftmostdigitre.match(stlasthalf);
                if(leftmostdigit_match):
                    stlasthalf = stlasthalf[:leftmostdigit_match.start(1)] + \
                            str(int(match.group(2)) + int(leftmostdigit_match.group(1))) + \
                            stlasthalf[leftmostdigit_match.start(2):];

                # replace exploded group with 0
                st = stfirsthalf + '0' + stlasthalf;
                break;

    # return in list form
    return True, eval(st)
    


def split(snailfish, logger):
    # find any numbers 10 or greater
    if(len(snailfish) < 2):
        return False, None
    did = False;
    if(isinstance(list, snailfish[0])):
        did, snailfish[0] = split(snailfish);
    else:
        if(snailfish[0] >= 10):
            snailfish[0] = [snailfish[0]/2, (snailfish[0]+1)/2];
            did = True
    if not did:
        if(isinstance(list, snailfish[1])):
            did, snailfish[1] = split(snailfish);
        else:
            if(snailfish[1] >= 10):
                snailfish[1] = [snailfish[1]/2, (snailfish[1]+1)/2];
                did = True
    
    return did, snailfish;


def reduce(snailfish, logger):
    did = True;
    while(did):
        did, snailfish = explode(snailfish, logger);
        if not did:
            did, snailfish = split(snailfish, logger);

def magnitude(snailfish):
    lhs_mag = snailfish[0];
    if(isinstance(snailfish[0], list)):
        lhs_mag = magnitude(snailfish[0]);
    rhs_mag = snailfish[1];
    if(isinstance(snailfish[1], list)):
        rhs_mag = magnitude(snailfish[1]);
    return 3*lhs_mag + 2*rhs_mag;


def test(logger):
    explode_testcases = [
        ([[[[3,4],1]]], True, [[[0,5]]]),
    ]

    nerrs = 0;

    for input, did, output in explode_testcases:
        calc_did, calc_output = explode(input, logger = logger);
        if(calc_did != did):
            print(f'testcase {str(input)}, expected explode {did}, got {calc_did}');
            nerrs += 1;
        elif(calc_output != output):
            print(f'testcase {str(input)}, expected output {output}, got {calc_output}');
            nerrs += 1;

    magnitude_testcases = [
            ([[1,2],[[3,4],5]], 143),
            ([[[[0,7],4],[[7,8],[6,0]]],[8,1]], 1384),
            ([[[[1,1],[2,2]],[3,3]],[4,4]], 445),
            ([[[[3,0],[5,3]],[4,4]],[5,5]], 791),
            ([[[[5,0],[7,4]],[5,5]],[6,6]], 1137),
            ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488),
    ]

    for input, answer in magnitude_testcases:
        calc_mag = magnitude(input);
        if(calc_mag != answer):
            print(f'magnitude testcase {input}: expected {answer}, got {calc_mag}');

    print(f"{nerrs} errors");
    return nerrs

if('__main__' == __name__):
    import argparse;

    # deal with command line arguments
    parser = argparse.ArgumentParser(
            description = 'Advent of Code {} day {} solution'.format(
                AOC_YEAR, AOC_DAY));
    logger = logging.Logger('AOC{}d{}'.format(AOC_YEAR, AOC_DAY));
    logger.addHandler(logging.StreamHandler());
    logger.setLevel(logging.INFO);

    parser.add_argument(
        '-2', '--part2', action='store_true',
        help='part 2?', default=False);
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='be verbose', default=False);
    parser.add_argument(
        '-T', '--test', action='store_true',
        help='run unit tests', default=False);

    args = parser.parse_args();
    if(args.verbose):
        logger.setLevel(logging.DEBUG);

    if(args.test):
        sys.exit(test(logger));

    line = sys.stdin.readline();
    snailfish = eval(line);
    line = sys.stdin.readline();
    while(line):
        snailfish = reduce([snailfish, eval(line)], logger);
        line = sys.stdin.readline();

    print(f'answer: {magnitude(snailfish)}')
