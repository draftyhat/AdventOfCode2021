import sys;
import logging;
import scanf;
import copy;

''' approach:
    assume each scanner overlaps at least 12 beacons with scanner0?
    input all beacons as points
    for each beacon in scanner0
     for each other scanner
      for each beacon in the other scanner
       assume this beacon is the indicated point in scanner0
       check to see if other points match up
    how to check to see if other points match up, given two beacons in two
    different scanners that we're going to assume are equivalent:
     try all rotations from the 24 possible
      for each point in the second scanner, calculate the position relative to
       scanner0 given the indicated translation/rotation. Verify that this
       point is either in scanner0's list or out of range of scanner0.
    24 rotations to consider. Map x,y,z to:
      x, y, z  x, z, y   y, x, z  y, z, x   z, y, x   y, z, x
     -x, y, z -x, z, y  -y, x, z -y, z, x  -z, y, x  -y, z, x
      x,-y, z  x,-z, y   y,-x, z  y,-z, x   z,-y, x   y,-z, x
      x, y,-z  x, z,-y   y, x,-z  y, z,-x   z, y,-x   y, z,-x
     -x,-y, z -x,-z, y  -y,-x, z -y,-z, x  -z,-y, x  -y,-z, x
     -x, y,-z -x, z,-y  -y, x,-z -y, z,-x  -z, y,-x  -y, z,-x
      x,-y,-z  x,-z,-y   y,-x,-z  y,-z,-x   z,-y,-x   y,-z,-x
     -x,-y,-z -x,-z,-y  -y,-x,-z -y,-z,-x  -z,-y,-x  -y,-z,-x
'''
''' approach #2: approach #1 was too computationally intense
from Reddit, calculate the distances between the beacons. This should map
beacon pairs to known beacon pairs. Find rotation, translation from this.
thanks to Praful for posting commented code!
https://github.com/Praful/advent_of_code/blob/main/2021/src/day19.jl
'''

AOC_DAY=19
AOC_YEAR=2021

ROTATIONS=[
   [ 1, 2, 3],[ 1, 3, 2],[ 2, 1, 3],[ 2, 3, 1],[ 3, 2, 1],[ 2, 3, 1],
   [-1, 2, 3],[-1, 3, 2],[-2, 1, 3],[-2, 3, 1],[-3, 2, 1],[-2, 3, 1],
   [ 1,-2, 3],[ 1,-3, 2],[ 2,-1, 3],[ 2,-3, 1],[ 3,-2, 1],[ 2,-3, 1],
   [ 1, 2,-3],[ 1, 3,-2],[ 2, 1,-3],[ 2, 3,-1],[ 3, 2,-1],[ 2, 3,-1],
   [-1,-2, 3],[-1,-3, 2],[-2,-1, 3],[-2,-3, 1],[-3,-2, 1],[-2,-3, 1],
   [-1, 2,-3],[-1, 3,-2],[-2, 1,-3],[-2, 3,-1],[-3, 2,-1],[-2, 3,-1],
   [ 1,-2,-3],[ 1,-3,-2],[ 2,-1,-3],[ 2,-3,-1],[ 3,-2,-1],[ 2,-3,-1],
   [-1,-2,-3],[-1,-3,-2],[-2,-1,-3],[-2,-3,-1],[-3,-2,-1],[-2,-3,-1],
]
ROTATIONS_2D=[
        [  1, 2], [ 2, 1],
        [ -1, 2], [-2, 1],
        [  1,-2], [ 2,-1],
        [ -1,-2], [-2,-1],
];

def translate(coords, translation):
    retval = [0] * len(coords);
    for i in range(len(translation)):
        retval[i] = coords[i] - translation[i];
    return retval;

def rotate(coords, rotation):
    retval = [0] * len(coords);
    for i in range(len(rotation)):
        retval[i] = coords[abs(rotation[i]) - 1];
        if rotation[i] < 0:
            retval[i] = 0 - retval[i];
    return retval;

def rotate_inverse(coords, rotation):
    # rotate 11 times
    retval = coords;
    for i in range(11):
        retval = rotate(retval, rotation);
    return retval;

def inrange(beacon, scanners = None, scannerrange = 1000):
    if(None == scanners):
        scanners = [ [0] * len(beacon) ];
    retval = False;
    for s in scanners:
        # if it's in range of any one scanner, it's in range.
        retval = True;
        for i in range(len(beacon)):
            if(abs(beacon[i] - s[i]) > scannerrange):
                retval = False;
                break;
        if retval:
            break;
    return retval;

def negate(coords):
    retval = [0] * len(coords);
    for i in range(len(coords)):
        retval[i] = 0 - coords[i];
    return retval;

def distance_squared(coord0, coord1):
    return sum([pow(coord0[i]-coord1[i],2) for i in range(len(coord0))]);

def get_scanner_location(pair0, pair1, rotations):
    # given two pair of beacons that we know map to each other, find the
    # translation/rotation required to map pair1 to pair0
    # (pair0 should always be scanner0)
    s0b0,s0b1 = pair0;
    s1b0,s1b1 = pair1;

    found = False;

    # try all rotations, calculate translation, verify translation is the same
    # for both points; if so, we've found the right rotation/translation
    for rotation in rotations:
        rotated_s0b0 = rotate(s0b0, rotation);
        rotated_s0b1 = rotate(s0b1, rotation);
        rotated_s1b0 = rotate(s1b0, rotation);
        rotated_s1b1 = rotate(s1b1, rotation);

        translation = [s1b0[i] - s0b0[i] for i in range(len(s0b0))];
        if translate(s1b1, translation) == s0b1:
            found = True;
            break;

        translation = [s1b1[i] - s0b0[i] for i in range(len(s0b0))];
        if translate(s1b0, translation) == s0b1:
            found = True;
            break;
    if found:
        return rotation, translation;

class scanner():
    def __init__(self, fh, name = None, beacons = None, rotations = ROTATIONS):
        self.mapped = False;
        self.ntries = 0;
        self.rotations = rotations;

        # read title line
        if name:
            self.name = name;
        else:
            self.name = str(scanf.scanf('--- scanner %d ---'));
        # read beacons
        if beacons:
            self.beacons = [tuple(b) for b in beacons];
        else:
            self.beacons = [];
            scanf_retval = scanf.scanf('%d,%d,%d');
            while(scanf_retval):
                self.beacons.append(tuple(scanf_retval));
                scanf_retval = scanf.scanf('%d,%d,%d');

        # create dictionary of distances between beacons
        self.beacon_distances = {};
        for idx, b0 in enumerate(self.beacons):
            for b1 in self.beacons[idx+1:]:
                self.beacon_distances[distance_squared(b0, b1)] = (b0, b1);

    def add_beacon(self, beacon):
        if not b in self.beacons:
            for b in self.beacons:
                self.beacon_distances[distance_squared(beacon, b)] = (beacon, b);
            self.beacons.append(beacon);

    def find_overlap(self, other, logger):
        logger.debug(f"Finding overlap between {self.name} and {other.name}");
        logger.debug(f"  self.distances : " + ",".join([str(x) for x in self.beacon_distances.keys()]));
        logger.debug(f"  other.distances: " + ",".join([str(x) for x in other.beacon_distances.keys()]));
        for distance in self.beacon_distances:
            if distance in other.beacon_distances:
                logger.debug(f"    found matching distance {distance}");
                return get_scanner_location(
                        other.beacon_distances[distance],
                        self.beacon_distances[distance],
                        self.rotations);


def coalesce_beacons(scanners, logger, scannerrange = 1000):
    # calculate translation, translate all beacons, put locations of all
    # beacons relative to the first scanner in our dictionary of beacons
    scanner0 = scanners.pop(0);
    scanner_location_list = [[0] * len(scanner0.beacons[0])];
    beacons = set();
    logger.debug(f"adding {len(scanner0.beacons)} from {scanner0.name} ({len(scanners)} scanners)");
    for b in scanner0.beacons:
        beacons.add(tuple(b));
    max_ntries = len(scanners);
    reps=0
    while len(scanners) > 0:
        reps += 1;
        if reps % 10 == 0:
            print(f"{reps}]: {len(scanners)} scanners");

        s = scanners.pop(0);
        logger.debug(f"=========== checking scanner {s.name}");
        answer = s.find_overlap(scanner0, logger);
        if answer is not None:
            rotation, translation = answer
            scanner_location_list.append(negate(translation));
            for b in s.beacons:
                s0.add_beacon(translate(rotate(b, rotation), translation));
            logger.debug(f"adding {len(s.beacons)} from {s.name}");
        else:
            # could not find location of this scanner. Try again later.
            s.ntries += 1;
            if s.ntries >= max_ntries:
                raise Exception(f"Scanner {s.name}: maxed out overlap" \
                        f" attempts.  Scanner list: {scanner_location_list}");
            scanners.append(s);

    return scanner0.beacons;


def test(logger):
    nerrs = 0;
    rotation_test_scanner = scanner(None, name = 'test',
            beacons = [[-1,-1,1],[-2,-2,2],[-3,-3,3],[-2,-3,1],[8,0,7],[5,6,-4]]);
    rotation_testcase_scanners = [
            scanner(None, '0',
                [[1,-1,1],[2,-2,2],[3,-3,3],[2,-1,3],[-8,-7,0],[-5,4,-6]]),
            scanner(None, '1',
                [[-1,-1,-1],[-2,-2,-2],[-3,-3,-3],[-1,-3,-2],[-7,0,8],[4,6,5]]),
            scanner(None, '2',
                [[1,1,-1],[2,2,-2],[3,3,-3],[1,3,-2],[7,0,8],[-4,-6,5]]),
            # rotation -2, 3, -1
            scanner(None, '3',
                [[1,1,1],[2,2,2],[3,3,3],[3,1,2],[0,7,-8],[-6,-4,-5]]),
            ];

    for s in rotation_testcase_scanners:
        # derive rotation based on last point
        rotation = [0,0,0]
        for idx in range(len(rotation)):
            try:
                rotation[idx] = rotation_test_scanner.beacons[-1].index(s.beacons[-1][idx]) + 1;
            except:
                rotation[idx] = -1 - rotation_test_scanner.beacons[-1].index(0 - s.beacons[-1][idx]);

        # rotate other beacons
        for beacon_idx in range(len(rotation_test_scanner.beacons) - 1):
            rotated = rotate(rotation_test_scanner.beacons[beacon_idx], rotation);
            if(rotated != s.beacons[beacon_idx]):
                print(f"ERROR: expected {rotation_test_scanner.beacons[beacon_idx]}" \
                        f" rotated by {rotation} to be {s.beacons[beacon_idx]};" \
                        f" got {rotated}");
                nerrs += 1;

    # full rotation/translation test
    rotation_translation_test_scanner = scanner(None,
            name = 'testscanner', beacons = [[-618,-824,-621],
                [-537,-823,-458],
                [-447,-329,318],
                [404,-588,-901],
                [544,-627,-890],
                [528,-643,409],
                [-661,-816,-575],
                [390,-675,-793],
                [423,-701,434],
                [-345,-311,381],
                [459,-707,401],
                [-485,-357,347],]);
    rotation_translation_test_scanner2 = scanner(None,
            name = 'testscanner2', beacons = [[686,422,578],
                [605,423,415],
                [515,917,-361],
                [-336,658,858],
                [-476,619,847],
                [-460,603,-452],
                [729,430,532],
                [-322,571,750],
                [-355,545,-477],
                [413,935,-424],
                [-391,539,-444],
                [553,889,-390],]);

    # ----- manual test
    test_s0_beacon = rotation_translation_test_scanner.beacons[0]
    beacon1 = rotation_translation_test_scanner2.beacons[0]
    rotation = [-1, 2, -3];
    translation = [-68,1246,43];
    answer0 = translate(rotate(beacon1, rotation), translation);
    expected0 = [-618,-824,-621];
    if answer0 != expected0:
        print(f"  rotation {rotation} translation {translation} of {beacon1}" \
                f" produced {answer0}, expected {expected0}")
        nerrs += 1;
    answer1 = translate(rotate(rotation_translation_test_scanner2.beacons[1], rotation), translation)
    expected1 = [-537,-823,-458];
    if answer1 != expected1:
        print(f"  rotation {rotation} translation {translation} of" \
                " {rotation_translation_test_scanner2.beacons[1]}" \
                f" produced {answer0}, expected {expected1}")
        nerrs += 1;

    rotated = rotate(beacon1, rotation);
    calc_translation = [rotated[0] - test_s0_beacon[0], rotated[1] - test_s0_beacon[1],
            rotated[2] - test_s0_beacon[2]];
    if calc_translation != translation:
        print(f"ERROR: calculated translation {calc_translation}, needed {translation}");
        nerrs += 1;

    for rotation in ROTATIONS:
        rotated = rotate(beacon1, rotation);
        translation = [rotated[0] - test_s0_beacon[0],
                rotated[1] - test_s0_beacon[1],
                rotated[2] - test_s0_beacon[2]];
        logger.debug(f"  {translation}  {rotation}  (rotated {rotated})");
        if list(translation) == calc_translation:
            logger.debug("-------- watch: should be the right translation!");
        for beacon_idx in range(1, len(rotation_translation_test_scanner2.beacons)):
            # 515,917,-361
            b = rotation_translation_test_scanner.beacons[beacon_idx];
            b2 = rotation_translation_test_scanner2.beacons[beacon_idx];
            mapped_b = translate(rotate(b2, rotation), translation);
            logger.debug(f"    {b2} mapped: {translate(rotate(b2, rotation), translation)}")
            if(mapped_b == list(b)):
                logger.debug(f"     !!!!!! found correct translation/rotation!");
            else:
                logger.debug(f"     :(   not the correct mapping: got {mapped_b} wanted {b}");
                break;
        if list(translation) == calc_translation:
            logger.debug("-------- done with correct translation!");

    # test known pair
    logger.debug(f"#### known pair test");
    answer = get_scanner_location(
            (rotation_translation_test_scanner.beacons[0],
             rotation_translation_test_scanner.beacons[1]),
            (rotation_translation_test_scanner2.beacons[0],
             rotation_translation_test_scanner2.beacons[1]),
            ROTATIONS);
    if answer is None:
        print(f"ERROR: didn't find scanner0/scanner1 first pair rotation/translation");
        nerrs += 1;
    else:
        rotation, translation = answer
        expected_rotation = [-1, 2, -3];
        if(expected_rotation != rotation):
            print(f"ERROR: unexpected rotation {rotation} calcluated from" \
                    f" scanner0/1 first pair. Expected {expected_rotation}");
            nerrs += 1;
        expected_translation = (-68,1246,43);
        if(expected_translation != tuple(translation)):
            print(f"ERROR: unexpected translation {translation} calcluated,"
                    f" expected {expected_translation}");
            nerrs += 1;

    sys.exit(nerrs);

    answer = rotation_translation_test_scanner2.find_overlap(
            rotation_translation_test_scanner, logger);
    if answer is None:
        print(f"ERROR: didn't find scanner2 rotation/translation");
        nerrs += 1;
    else:
        rotation, translation = answer
        expected_rotation = [-1, 2, -3];
        if(expected_rotation != rotation):
            print(f"ERROR: unexpected rotation {rotation} calcluated, expected " \
                    f"{expected_rotation}");
            nerrs += 1;
        expected_translation = (-68,1246,43);
        if(expected_translation != tuple(translation)):
            print(f"ERROR: unexpected translation {translation} calcluated, expected " \
                    f"{expected_translation}");
            nerrs += 1;

    print(f"{nerrs} errors");
    return nerrs;

def test_rotation(logger):
    nerrs = 0;

    # create testcases
    testcases3d = []
    for r in ROTATIONS:
        testcases3d.append(rotate([3,4,5], r));
        testcases3d.append(rotate([-3,-2,-4], r));


    calculated_ntimes = 0;
    for r in ROTATIONS:
        for testcase in testcases3d:
            print(f"=== testing rotation {r} testcase {testcase}");
            rotated = rotate(testcase, r);
            ntimes = 1;
            while testcase != rotated:
                logger.debug(f"  testcase {testcase} rotation {r}  {ntimes:2d}: {rotated}");
                ntimes += 1
                rotated = rotate(rotated, r);
            calculated_ntimes = max(calculated_ntimes, ntimes);
    print(f" rotation test calculated ntimes: {calculated_ntimes}");

    for r in ROTATIONS:
        logger.debug(f'-- testing 3d rotation {r}');
        for testcase in testcases3d:
            # rotate 12 times
            rotated = rotate(testcase, r);
            answer = rotate_inverse(rotated, r);
            if(answer != testcase):
                nerrs += 1;
                logger.debug(f"---- rotation failed, testcase {testcase}, answer {answer}");

    print(f"rotation test: {nerrs} errors");
    return nerrs;



def test2d(logger):
    nerrs = 0;

    scanners = [
        scanner(None, name = 's0', beacons = [ [-1,3],[-3,1],[-6,6] ],
            rotations = ROTATIONS_2D),
        scanner(None, name = 's1', beacons = [ [-9,7],[-7,9],[1,1]],
            rotations = ROTATIONS_2D),
        scanner(None, name = 's2',
            beacons = [ [7,9],[9,7],[4,4],[-3,-1],[-1,-3] ],
            rotations = ROTATIONS_2D),
    ];

    beacons = coalesce_beacons(scanners, scannerrange = 10, logger = logger);
    if len(beacons) != 6:
        print(f"ERROR: expected 6 beacons, found {len(beacons)}");
        nerrs += 1;

    print("2d beacons: " + '  '.join([str(x) for x in beacons]));
    print(f"{nerrs} 2d errors");
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
        help='be verbose', default=False);

    args = parser.parse_args();
    if(args.verbose):
        logger.setLevel(logging.DEBUG);

    if(args.test):
        nerrs = test(logger);
        #nerrs += test2d(logger);
        #nerrs += test_rotation(logger);
        sys.exit(nerrs);

    # read scanners/beacons
    scanners = []
    line = sys.stdin.readline();
    while(line):
        scanners.append(scanner(sys.stdin, name = line.strip()));
        line = sys.stdin.readline();

    beacons = coalesce_beacons(scanners, logger = logger);
    print(f"Found {len(beacons)} beacons");
    l = [str(x).strip('()') for x in beacons];
    l.sort();
    print('\n'.join(l));
