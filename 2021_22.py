import sys;
import logging;
import scanf;

AOC_DAY=22
AOC_YEAR=2021

class region():
    def __init__(self, line, logger):
        self.logger = logger;

        # read from stdin
        (onoff, self.x0, self.x1, self.y0, self.y1, self.z0, self.z1) = \
                scanf.scanf("%s x=%d..%d,y=%d..%d,z=%d..%d", line);

        self.on = True if 'on' == onoff else False;

    def __repr__(self):
        print(self.__dict__);
        retval = 'on ' if self.on else 'off ';
        retval += f'x = {self.x0}..{self.x1}' \
                f',y = {self.y0}..{self.y1}' \
                f',z = {self.z0}..{self.z1}';
        return retval;

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

    regionlist = [];
    line = sys.stdin.readline();
    while(line):
        # read new region
        newregions = [region(line, logger)];
        # compute intersection with all other regions and add to list
        new_regionlist = [];
        for r in regionlist;
            for newr in newregions:
                if(r.intersects(newr)):

        regionlist = new_regionlist;
        regionlist.extend(newregions);

            

        line = sys.stdin.readline();


