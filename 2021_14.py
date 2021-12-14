import sys;
import logging;

AOC_DAY=14
AOC_YEAR=2021

def read_formulae(logger):
    formulae = {};
    line = sys.stdin.readline().strip();
    while(line):
        pair, insertch = line.split(' -> ');
        formulae[pair] = insertch;
        line = sys.stdin.readline().strip();

    return formulae;

def calculate_polymer(formulae, initial_polymer):
    retval = initial_polymer[0]
    for pairindex in range(len(initial_polymer)-1):
        retval += formulae[initial_polymer[pairindex:pairindex + 2]] \
                + initial_polymer[pairindex + 1];
    return retval;

def count_chars(chars, polymer):
    for ch in polymer:
        chars[ch] = chars.get(ch, 0) + 1;


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

    # calculate the result for each pair
    nsteps = 10;
    # we initialize this array with the first character
    chars = { initial_polymer[0]: 1 };
    for i in range(len(initial_polymer) - 1):
        step_polymer = initial_polymer[i:i+2];
        print("processing step_polymer {}".format(step_polymer));
        for step in range(nsteps):
            step_polymer = calculate_polymer(formulae, step_polymer);
        # don't count the first character, which was counted in the last polymer
        count_chars(chars, step_polymer[1:]);

    # find max and min occurrences
    (maxch, maxoccurrences) = chars.popitem();
    (minch, minoccurrences) = (maxch, maxoccurrences);
    for (ch, occurrences) in chars.items():
        if(occurrences > maxoccurrences):
            maxch = ch;
            maxoccurrences = occurrences;
        if(occurrences < minoccurrences):
            minch = ch;
            minoccurrences = occurrences;

    logger.debug(f'After {nsteps} steps, max {maxch} with {maxoccurrences}' \
            f', min {minch} with {minoccurrences}');

    print(maxoccurrences - minoccurrences);

