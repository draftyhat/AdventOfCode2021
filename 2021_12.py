import sys;
import logging;

AOC_DAY=12
AOC_YEAR=2021

class cave():
    def __init__(self, name):
        self.name = name;
        self.big = False;
        self.start = False;
        self.end = False;
        if(self.name[0].upper() == self.name[0]):
            self.big = True;
        elif(self.name == 'start'):
            self.start = True;
        elif(self.name == 'end'):
            self.end = True;
        self.connected_to = []

    def add_connected(self, c):
        self.connected_to.append(c)
        self.connected_to.sort();

    def find_next(self, path):
        # return a sorted list of options for the next cave to visit
        retval = [];
        for i in self.connected_to:
            if i.big or not i in path:
                retval.append(i);
        return retval;

    def __eq__(self, other):
        if type(other) == str:
            return self.name == other;
        return self.name == other.name;
    def __lt__(self, other):
        if(self.end or other.start):
            return False;
        if(other.end or self.start):
            return True;
        return self.name < other.name;

    def __repr__(self):
        return self.name;


def count_paths(start, path, logger):
    npaths = 0;
    for next_path in start.find_next(path):
        if(next_path.end):
            npaths += 1;
            logger.debug("found path {}".format(path + [next_path]));
        else:
            npaths += count_paths(next_path, path + [next_path], logger);

    return npaths;

def read_caves():
    caves = [];
    cave_names = [];
    start = None;
    line = sys.stdin.readline().strip();
    while(line):
        (cave1_name, cave2_name) = line.split('-');
        try:
            cave1 = caves[caves.index(cave1_name)]
        except Exception as e:
            cave1 = cave(cave1_name);
            caves.append(cave1);
        try:
            cave2 = caves[caves.index(cave2_name)]
        except:
            cave2 = cave(cave2_name);
            caves.append(cave2);
        cave1.add_connected(cave2);
        cave2.add_connected(cave1);
        if start is None and cave1.start:
            start = cave1;
        elif start is None and cave2.start:
            start = cave2;
        line = sys.stdin.readline().strip();

    print(caves);

    return start;

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

    start = read_caves();
    npaths = count_paths(start, [start], logger);
    print(npaths);

