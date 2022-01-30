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
        self_retval = [];
        other_retval = [];
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
                                logger.debug(f"   get_intersections processing {r}");
                                if(self.contains(r)):
                                    # note that we return the yet-unintersected
                                    # parts of off regions too, so they can
                                    # continue to be processed (in case they
                                    # intersect other regions).
                                    r.on = self.on;
                                    self_retval.append(r);
                                elif (other.contains(r)):
                                    logger.debug(f"    {r} in other");
                                    if(other.on):
                                        r.on = other.on;
                                        other_retval.append(r);
                                # otherwise this region is not in either self
                                # or other; leave it.
        logger.debug(f"get_intersections return self {'|'.join([str(x) for x in self_retval])}");
        logger.debug(f"get_intersections return other {'|'.join([str(x) for x in other_retval])}");
        return self_retval, other_retval;

    def size(self):
        if not self.on:
            return 0;
        print("{}-{} x {}-{} x {}-{} = {} * {} * {} = {}".format(self.x0, self.x1, self.y0, self.y1, self.z0, self.z1, self.x1 - self.x0,self.y1 - self.y0, self.z1 - self.z0, (self.x1 - self.x0) * (self.y1 - self.y0) * (self.z1 - self.z0)));
        return (self.x1 - self.x0) * (self.y1 - self.y0) * (self.z1 - self.z0);

    def get_cubes(self):
        retval = [];
        if not self.on:
            for x in range(self.x0, self.x1):
                for y in range(self.y0, self.y1):
                    for z in range(self.z0, self.z1):
                        retval.append((x,y,z));
        return retval;
    
    def __repr__(self):
        retval = 'on ' if self.on else 'off ';
        retval += f'x = {self.x0}..{self.x1 - 1}' \
                f',y = {self.y0}..{self.y1 - 1}' \
                f',z = {self.z0}..{self.z1 - 1}';
        return retval;

def get_n_cubes(lines, logger):
    print("lines:")
    print(lines);
    regionlist = [region(lines[0])];
    for line in lines[1:]:
        # read new region
        read_region = region(line = line);
        newregions = [read_region];
        logger.debug("adding new region {}".format(read_region));

        # compute intersection with all other regions and add to list
        #  regionlist holds the existing list of regions
        #  newregions will hold the regions being added (the new one gets split
        #  as we go)
        #  new_regionlist will hold the result after adding newregions

        new_regionlist = [];
        new_newregions = [];
        for r in regionlist:
            logger.debug(f"-- intersecting new {'|'.join([str(n) for n in newregions])} with region {r}");
            intersected = False;
            new_newregions = [];
            while len(newregions) > 0:
                newr = newregions.pop();
                logger.debug("    adding new {}".format(newr));
                if(newr.intersects(r)):
                    newsplit, rsplit = newr.get_intersections(r);
                    intersected = True;
                    new_newregions.extend(newsplit);
                    new_regionlist.extend(rsplit);
                else:
                    new_newregions.append(newr);

            newregions = new_newregions;
            if not intersected:
                new_regionlist.append(r);

        regionlist = new_regionlist;
        regionlist.extend(newregions);
        logger.debug("-- current region list {}".format(
            '\n'.join([str(r) for r in regionlist])));
        for r in regionlist:
            logger.debug(f'*** {r}\n  ' + '\n  '.join([str(c) for c in r.get_cubes()]));

        line = sys.stdin.readline();

    logger.debug("final region list\n  {}".format('\n  '.join([str(r) for r in regionlist])));
    turned_on = 0;
    cubes = [];
    for r in regionlist:
        turned_on += r.size();
        cubes.extend(r.get_cubes());

    print("{} cubes turned on.".format(turned_on));
    print(f"{len(cubes)} distinct cubes");
    cubes.sort(key=lambda x:x[0] * 10000 + x[1] * 100 + x[2]);
    print('\n'.join([str(x) for x in cubes]));

    return turned_on;


def test(logger):
    nerrs = 0;

    # unit test contains()
    contains_testcases = [
            ('on x=1..1,y=1..1,z=1..1',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=1..2,y=1..1,z=1..1',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=1..1,y=1..2,z=1..1',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=1..1,y=1..1,z=1..2',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=0..1,y=1..1,z=1..1',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=1..1,y=0..1,z=1..1',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=1..1,y=1..1,z=0..1',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=0..2,y=1..1,z=1..1',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=1..1,y=0..2,z=1..1',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=1..1,y=1..1,z=0..2',
             'on x=1..1,y=1..1,z=1..1', True),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=0..1,y=1..1,z=1..1', False),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=1..1,y=0..1,z=1..1', False),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=1..1,y=1..1,z=0..1', False),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=1..2,y=1..1,z=1..1', False),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=1..1,y=1..2,z=1..1', False),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=1..1,y=1..1,z=1..2', False),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=0..2,y=1..1,z=1..1', False),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=1..1,y=0..2,z=1..1', False),
            ('on x=1..1,y=1..1,z=1..1',
             'on x=1..1,y=1..1,z=0..2', False),
    ];
    for container_line, newregion_line, contains in contains_testcases:
        container = region(line = container_line);
        newregion = region(line = newregion_line);
        answer = container.contains(newregion);
        if answer != contains:
            nerrs = nerrs + 1;
            print(f"ERROR: contains test, expected" \
                  f" {container}.contains({newregion}) {contains}," \
                  f" got {answer}");


    intersects_testcases = [
        ('on x=10..12,y=10..12,z=10..12',
         'on x=10..12,y=10..12,z=10..12',
         ['on x=10..12,y=10..12,z=10..12',], []),
        ('on x=10..12,y=10..12,z=10..12',
         'on x=11..12,y=11..12,z=12..12',
         ['on x=10..12,y=10..12,z=10..12',], []),
    ];

'on x = 10..10,y = 10..10,z = 10..11',
'on  x = 10..10,y = 10..10,z = 12..12',
'on  x = 10..10,y = 11..12,z = 10..11',
'on  x = 10..10,y = 11..12,z = 12..12',
'on  x = 11..12,y = 10..10,z = 10..11',
'on  x = 11..12,y = 10..10,z = 12..12',
'on  x = 11..12,y = 11..12,z = 10..11',
'on  x = 11..12,y = 11..12,z = 12..12']

    for r0_line, r1_line, selflist, otherlist in intersects_testcases:
        r0 = region(line = r0_line);
        r1 = region(line = r1_line);
        selflist_answer, otherlist_answer = r0.get_intersections(r1);
        if selflist_answer != selflist:
            nerrs = nerrs+1;
            print(f"ERROR: intersects test\n  {r0}\n  {r1}\n" \
                    f"  selflist {selflist_answer}\n" \
                    f"  expected {selflist}")
        if otherlist_answer != otherlist:
            nerrs = nerrs+1;
            print(f"ERROR: intersects test\n  {r0}\n  {r1}\n" \
                    f"  otherlist {otherlist_answer}\n" \
                    f"  expected  {otherlist}")

    test_problem_lines = [
        ];
    '''
            (['on x=10..12,y=10..12,z=10..12'], 27),
            (['on x=10..12,y=10..12,z=10..12',
              'on x=11..13,y=11..13,z=11..13'], 46),
            (['on x=10..12,y=10..12,z=10..12',
              'on x=11..13,y=11..13,z=11..13',
              'off x=9..11,y=9..11,z=9..11'], 38),
        ];
            (['on x=10..12,y=10..12,z=10..12',
              'on x=11..13,y=11..13,z=11..13',
              'off x=9..11,y=9..11,z=9..11',
              'on x=10..10,y=10..10,z=10..10'], 39),
        ];
    '''

    for nlines in range(len(test_problem_lines)):
        lines, expected_n_cubes = test_problem_lines[nlines];
        answer = get_n_cubes(lines, logger);
        if(answer != expected_n_cubes):
            print(f"ERROR: {nlines + 1} test lines, expected answer" \
                    f" {answer}, received answer {expected_n_cubes}");
            nerrs = nerrs + 1;

    print(f"{nerrs} errors");
    return nerrs;


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
        help='run unit test', default=False);

    args = parser.parse_args();
    if(args.verbose):
        logger.setLevel(logging.DEBUG);

    if(args.test):
        sys.exit(test(logger));

    print(f"Found {get_n_cubes(sys.stdin.readlines(), logger)} cubes");

