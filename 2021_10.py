import sys;
import logging;

AOC_DAY=10
AOC_YEAR=2021

chunk_characters = {
        '(':')',
        '[':']',
        '{':'}',
        '<':'>',
}
illegal_character_score = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
}
complete_character_score = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
};

def is_corrupted(line, logger):
    # return (score of corrupted line; score of incomplete line)
    # incomplete_score: of corrupted line; 0 if valid
    # complete_score: of incomplete line
    match = [];
    for ch in line:
        if ch in chunk_characters:
            match.append(chunk_characters[ch]);
        elif ch in illegal_character_score:
            try:
                p = match.pop();
            except:
                p = '';
            if(p != ch):
                logger.debug(" Found illegal character {} (should have" \
                        " matched {})! Returning {}.".format(ch, p,
                            illegal_character_score[ch]));
                return (illegal_character_score[ch], 0);
        else:
            raise Exception("Unrecognized character {}!".format(ch));

    print("---------- match {}".format(match));
    incomplete_score = 0;
    match.reverse();
    for ch in match:
        print("-- ch adds {} to {}".format(ch, incomplete_score));
        incomplete_score = incomplete_score * 5 + complete_character_score[ch];
    return (0, incomplete_score);


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

    illegal_score = 0;
    incomplete_score = [];
    line = sys.stdin.readline().strip();
    while len(line) > 0:
        logger.debug("parsing line {}".format(line));
        (illegal_line_score, incomplete_line_score) = is_corrupted(line, logger)
        illegal_score += illegal_line_score;
        if(0 == illegal_line_score):
            incomplete_score.append(incomplete_line_score);
        line = sys.stdin.readline().strip();

    print(illegal_score);
    incomplete_score.sort();
    print(incomplete_score);
    print(incomplete_score[int(len(incomplete_score)/2)]);



# guesses: 5849401116 (too high)
