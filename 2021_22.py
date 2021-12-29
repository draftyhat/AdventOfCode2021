# buggy. Gets first 2 lines of first test right, but wrong answer with 3 lines.
# Gets this right:
# echo -e "on x=0..2,y=0..2,z=0..2\noff x=0..1,y=0..1,z=0..1" | python3 2021_22.py  -v

import sys;
import logging;
import scanf;

AOC_DAY=22
AOC_YEAR=2021

class region():
    def __init__(self, line = None,
            x0 = 0, x1 = 0, y0 = 0, y1 = 0, z0 = 0, z1 = 0):
        self.logger = logger;
        self.on = None;
        self.x0 = x0;
        self.x1 = x1;
        self.y0 = y0;
        self.y1 = y1;
        self.z0 = z0;
        self.z1 = z1;

        # read from stdin
        if(line):
            (onoff, self.x0, self.x1, self.y0, self.y1, self.z0, self.z1) = \
                    scanf.scanf("%s x=%d..%d,y=%d..%d,z=%d..%d", line);
            # assume n0 < n1 for all n x,y,z. This needs to be true for our
            # intersection calculations.

            self.on = True if 'on' == onoff else False;
            # input regions are [], we want [)
            self.x1 += 1;
            self.y1 += 1;
            self.z1 += 1;

    def intersects(self, other):
        ''' one line segment x0,x1, other.x0, other.x1 if:
             x0 <= other.x0 <= x1 OR
             x0 <= other.x1 <= x1 OR
             other.x0 < x0 and x1 < other.x1
            to get an intersection in 3d, we need this for all axes.
        '''
        return ((self.x0 <= other.x0 and other.x0 <= self.x1)
                or (self.x0 <= other.x1 and other.x1 <= self.x1)
                or (other.x0 < self.x0 and self.x1 < other.x1)) \
           and ((self.y0 <= other.y0 and other.y0 <= self.y1)
                or (self.y0 <= other.y1 and other.y1 <= self.y1)
                or (other.y0 < self.y0 and self.y1 < other.y1)) \
           and ((self.z0 <= other.z0 and other.z0 <= self.z1)
                or (self.z0 <= other.z1 and other.z1 <= self.z1)
                or (other.z0 < self.z0 and self.z1 < other.z1));

    def contains(self, other):
        return ((self.x0 <= other.x0)
                and (other.x1 <= self.x1)
                and (self.y0 <= other.y0)
                and (other.y1 <= self.y1)
                and (self.z0 <= other.z0)
                and (other.z1 <= self.z1));

    def get_intersections(self, other):
        retval = [];
        self.logger.debug("get_intersections({}, {})".format(
            str(self), str(other)));
        # assume this region intersects with the other
        # assume this region is the newer region, other is the older
        #  collect all points and sort
        #  tuple is: value, on/off to the right, on/off to the left, newer
        xs = [self.x0, self.x1, other.x0, other.x1];
        ys = [self.y0, self.y1, other.y0, other.y1];
        zs = [self.z0, self.z1, other.z0, other.z1];
        xs.sort();
        ys.sort();
        zs.sort();
        self.logger.debug("  xs {} ys {} zs {}".format(xs, ys, zs));
        for xindex in range(1, len(xs)):
            if(xs[xindex - 1] != xs[xindex]):
                for yindex in range(1, len(ys)):
                    if(ys[yindex - 1] != ys[yindex]):
                        for zindex in range(1, len(zs)):
                            if(zs[zindex - 1] != zs[zindex]):
                                r = region(x0 = xs[xindex - 1], x1 = xs[xindex],
                                        y0 = ys[yindex - 1], y1 = ys[yindex],
                                        z0 = zs[zindex - 1], z1 = zs[zindex]);
                                if(self.contains(r)):
                                    if(self.on):
                                        r.on = self.on;
                                        retval.append(r);
                                elif (other.contains(r)):
                                    if(other.on):
                                        r.on = other.on;
                                        retval.append(r);
                                # otherwise this region is not in either self
                                # or other; leave it.
        return retval;

    def size(self):
        print("{}-{} x {}-{} x {}-{} = {} * {} * {} = {}".format(self.x0, self.x1, self.y0, self.y1, self.z0, self.z1, self.x1 - self.x0,self.y1 - self.y0, self.z1 - self.z0, (self.x1 - self.x0) * (self.y1 - self.y0) * (self.z1 - self.z0)));
        return (self.x1 - self.x0) * (self.y1 - self.y0) * (self.z1 - self.z0);
    
    def __repr__(self):
        retval = 'on  ' if self.on else 'off ';
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
        newregions = [region(line = line)];
        logger.debug("adding new region {}".format(newregions[0]));

        # compute intersection with all other regions and add to list

        new_regionlist = [];
        for r in regionlist:
            print("-- intersecting new with region {}".format(r));
            new_newregions = [];
            intersected = False;
            print(" -- newregions length {}".format(len(newregions)));
            for newr in newregions:
                #print("-- adding new {}".format(newr));
                if(r.intersects(newr)):
                    new_newregions.extend(newr.get_intersections(r));
                    intersected = True;
                else:
                    new_newregions.append(newr);

            newregions = new_newregions;
            if not intersected:
                new_regionlist.append(r);

        regionlist = new_regionlist;
        regionlist.extend(newregions);
        logger.debug("-- current region list {}".format(
            '\n'.join([str(r) for r in regionlist])));

        line = sys.stdin.readline();

    logger.debug("final region list\n  {}".format('\n  '.join([str(r) for r in regionlist])));
    turned_on = 0;
    for r in regionlist:
        turned_on += r.size();

    print("{} cubes turned on.".format(turned_on));
