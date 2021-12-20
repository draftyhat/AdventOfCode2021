import sys;
import logging;

AOC_DAY=14
AOC_YEAR=2021

def read_formulae(logger):
    formulae = {};
    line = sys.stdin.readline().strip();
    while(line):
        pair, insertch = line.split(' -> ');
        formulae[pair] = (pair[0] + insertch, insertch + pair[1]);
        line = sys.stdin.readline().strip();

    return formulae;

def step_polymer(formulae, countdict):
    retval = {};
    for (digraph, count) in countdict.items():
        (new_digraph0, new_digraph1) = formulae[digraph];
        retval[new_digraph0] = retval.get(new_digraph0, 0) + count;
        retval[new_digraph1] = retval.get(new_digraph1, 0) + count;
    return retval;

def count_min_max(firstletter, countdict):
    lettercounts = {};
    for (digraph, count) in countdict.items():
        lettercounts[digraph[1]] = lettercounts.get(digraph[1], 0) + count;
    lettercounts[firstletter] = lettercounts.get(firstletter, 0) + 1;

    sorted_counts = [x for x in lettercounts.items()];
    sorted_counts.sort(key = lambda x: x[1]);
    print(sorted_counts);
    return(sorted_counts[0][1], sorted_counts[-1][1]);

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

    args = parser.parse_args();
    if(args.verbose):
        logger.setLevel(logging.DEBUG);

    # read the initial polymer
    initial_polymer = sys.stdin.readline().strip();
    # skip a line
    sys.stdin.readline();
    # read the directions
    formulae = read_formulae(logger);

    # initialize the count dictionary
    countdict = {}
    for i in range(len(initial_polymer) - 1):
        digraph = initial_polymer[i:i+2];
        countdict[digraph] = countdict.get(digraph, 0) + 1;
    print(countdict);

    # step the dictionary 10 times, and run counts
    for i in range(10):
        countdict = step_polymer(formulae, countdict);

    # print out counts
    (min, max) = count_min_max(initial_polymer[0], countdict);
    print(max - min);

    # step to 40
    for i in range(30):
        countdict = step_polymer(formulae, countdict);

    # print out counts
    (min, max) = count_min_max(initial_polymer[0], countdict);
    print(max - min);

