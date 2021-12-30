import sys;
import logging;
import re;
import math;

AOC_DAY=14
AOC_YEAR=2021


pairherere = re.compile('^(\d+),(\d+)(.*)');
#rightmostdigitre = re.compile('.*(\d+)([^\d]*)');
#leftmostdigitre = re.compile('[^\d]*(\d+)(.*)');
rightmostdigitre = re.compile('.*?(\d+)([^\d]*)$');
leftmostdigitre = re.compile('^[^\d]*(\d+)(.*?)');

def explode(snailfish, logger):
    logger.debug(f'explode: {snailfish}');
    # find the leftmost depth-4 pair and explode it.
    # work with the text representation of the number (no spaces)
    did = False
    st = str(snailfish).replace(' ','');
    depth = 0;
    last_number_index = None;
    for index, item in enumerate(st):
        if '[' == item:
            depth += 1;
        elif ']' == item:
            depth -= 1;
        elif depth > 4:
            logger.debug(f'explode: depth {depth} at {index} "{st[index:]}"');
            # find out if there's a pair here
            match = pairherere.match(st[index:]);
            if(match):
                # explode this pair
                stfirsthalf = st[:index-1];
                stlasthalf = st[index + match.start(3)+1:];
                # new string will be firsthalf 0 lasthalf
                # add first in matched pair to rightmost digit preceding match
                rightmostdigit_match = rightmostdigitre.match(stfirsthalf);
                if(rightmostdigit_match):
                    stfirsthalf = stfirsthalf[:rightmostdigit_match.start(1)] + \
                            str(int(match.group(1)) + int(rightmostdigit_match.group(1))) + \
                            stfirsthalf[rightmostdigit_match.start(2):];
                    logger.debug(f"explode:  first half {stfirsthalf}");

                # add last in matched pair to leftmost digit following match
                leftmostdigit_match = leftmostdigitre.match(stlasthalf);
                if(leftmostdigit_match):
                    stlasthalf = stlasthalf[:leftmostdigit_match.start(1)] + \
                            str(int(match.group(2)) + int(leftmostdigit_match.group(1))) + \
                            stlasthalf[leftmostdigit_match.start(2):];
                    logger.debug(f"explode:   last half {stlasthalf}");

                # replace exploded group with 0
                st = stfirsthalf + '0' + stlasthalf;
                did = True;
                break;

    # return in list form
    return did, eval(st)
    


def split(snailfish, logger):
    logger.debug(f"split: {snailfish}");
    # find any numbers 10 or greater
    if(len(snailfish) < 2):
        return False, None
    did = False;
    if(isinstance(snailfish[0], list)):
        did, snailfish[0] = split(snailfish[0], logger);
    else:
        if(snailfish[0] >= 10):
            snailfish[0] = [math.floor(snailfish[0]/2), math.ceil(snailfish[0]/2)];
            did = True
    if not did:
        if(isinstance(snailfish[1], list)):
            did, snailfish[1] = split(snailfish[1], logger);
        else:
            if(snailfish[1] >= 10):
                snailfish[1] = [math.floor(snailfish[1]/2), math.ceil(snailfish[1]/2)];
                did = True
    
    return did, snailfish;


def reduce(snailfish, logger):
    did = True;
    while(did):
        did, snailfish = explode(snailfish, logger);
        if not did:
            did, snailfish = split(snailfish, logger);
            logger.debug(f" split result: {snailfish}");
        print(f"step: {snailfish}");
    return snailfish

def magnitude(snailfish):
    lhs_mag = snailfish[0];
    if(isinstance(snailfish[0], list)):
        lhs_mag = magnitude(snailfish[0]);
    rhs_mag = snailfish[1];
    if(isinstance(snailfish[1], list)):
        rhs_mag = magnitude(snailfish[1]);
    return 3*lhs_mag + 2*rhs_mag;


#def test(logger):
#    #input = [[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]], [2, 9]]
#    #output = reduce(input, logger = logger);
#    input= [[[[12, 12], [6, 14]], [[15, 0], [17, [8, 1]]]], [2, 9]];
#    print(f"input:  {input}");
#    did,output=explode(input, logger = logger)
#    print(f"result: {output}");

def test(logger):
    nerrs = 0;

    explode_testcases = [
        ([[[[[3,4],1]]]], True, [[[[0,5]]]]),
        ([[[[[9,8],1],2],3],4], True, [[[[0,9],2],3],4]),
        ([7,[6,[5,[4,[3,2]]]]], True, [7,[6,[5,[7,0]]]]),
        ([[6,[5,[4,[3,2]]]],1], True, [[6,[5,[7,0]]],3]),
    ]

    for input, did, output in explode_testcases:
        calc_did, calc_output = explode(input, logger = logger);
        if(calc_did != did):
            print(f'testcase {str(input)}, expected explode {did}, got {calc_did}');
            nerrs += 1;
        elif(calc_output != output):
            print(f'testcase {str(input)}, expected output {output}, got {calc_output}');
            nerrs += 1;

    reduce_testcases = [
            ([[[[1,1],[2,2]],[3,3]],[4,4]], [[[[1,1],[2,2]],[3,3]],[4,4]]),
            ([[[[[1,1],[2,2]],[3,3]],[4,4]],[5,5]], [[[[3,0],[5,3]],[4,4]],[5,5]]),
            ([[[[[[1,1],[2,2]],[3,3]],[4,4]],[5,5]],[6,6]], [[[[5,0],[7,4]],[5,5]],[6,6]]),
            ([[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]], [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]),
            ([[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
                ,[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]], [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]),
            ([[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]],
                [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]),
            ([[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]],
                [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]),

            ([[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],[[2,[2,2]],[8,[8,1]]]],
                [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]),

            ([[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],[2,9]],
                [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]),

            #([[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],[1,[[[9,3],9],[[9,0],[0,7]]]]],
            #    [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]),

            #([[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],[[[5,[7,4]],7],1]],
            #    [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]),

            #([[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],[[[[4,2],2],6],[8,7]]],
            #    [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]),
        ]

    '''
[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
[[[[4,0],[5,4]],[[0,[7,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
[[[[4,0],[5,4]],[[7,0],[15,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
[[[[4,0],[5,4]],[[7,15],0]],[12,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
[[[[4,0],[5,4]],[[7,15],0]],[15,[[0,[11,3]],[[6,3],[8,8]]]]]
[[[[4,0],[5,4]],[[7,15],0]],[15,[[11,0],[[9,3],[8,8]]]]]
[[[[4,0],[5,4]],[[7,15],0]],[15,[[11,9],[0,[11,8]]]]]
[[[[4,0],[5,4]],[[7,15],0]],[15,[[11,9],[11,0]]]]
[[[[4,0],[5,4]],[[7,[7, 8]],0]],[15,[[11,9],[11,0]]]]
[[[[4,0],[5,4]],[[14,0],8]],[15,[[11,9],[11,0]]]]
[[[[4,0],[5,4]],[[[7, 7],0],8]],[15,[[11,9],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[15,[[11,9],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[7, 8],[[11,9],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[7, 8],[[[5, 6],9],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[7, 13],[[0,15],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[7, [6, 7]],[[0,15],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[13, 0],[[7,15],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 0],[[7,15],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 0],[[7,[7,8]],[11,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 0],[[14,0],[19,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 0],[[[7,7],0],[19,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[0,7],[19,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[0,7],[[9,10],0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[0,16],[0,10]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[0,[8,8]],[0,10]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[8,8],[8,10]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[8,8],[8,[5,5]]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[8,8],[13,0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[8,8],[[6,7],0]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[8,14],[0,7]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[8,[7,7]],[0,7]]]]
[[[[4,0],[5,11]],[[0,7],8]],[[[6,7], 7],[[15,0],[7,7]]]]
[[[[4,0],[5,[5,6]]],[[0,7],8]],[[[6,7], 7],[[15,0],[7,7]]]]
[[[[4,0],[10,0]],[[6,7],8]],[[[6,7], 7],[[15,0],[7,7]]]]
[[[[4,0],[[5,5],0]],[[6,7],8]],[[[6,7], 7],[[15,0],[7,7]]]]
[[[[4,5],[0,5]],[[6,7],8]],[[[6,7], 7],[[15,0],[7,7]]]]



    '''

    for input, output in reduce_testcases:
        calc_output = reduce(input, logger);
        if(calc_output != output):
            print(f'reduce testcase {str(input)}, expected output:\n   {output}\n got:\n   {calc_output}');
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
            nerrs += 1;

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
        logger.debug("-- adding line {}".format(line));
        snailfish = reduce([snailfish, eval(line)], logger);
        line = sys.stdin.readline();

    print(f'answer: {magnitude(snailfish)}')
