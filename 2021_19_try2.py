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
answers
 scanner 1 at [68, -1246, -43]  r=[-1, 2, -3]  t=[-68, 1246, 43]i
 scanner 4 at [-20, -1133, 1061]  r=[-2,-3,1]  t=[20,1133,-1061]
 scanner 2 at [1105,-1205,1229]
 scanner 3 at [-92,-2380,-20]
'''

AOC_DAY=19
AOC_YEAR=2021

ROTATIONS=[
   [ 1, 2, 3],[ 1, 3, 2],[ 2, 1, 3],[ 2, 3, 1],[ 3, 2, 1],[ 3, 1, 2],
   [-1, 2, 3],[-1, 3, 2],[-2, 1, 3],[-2, 3, 1],[-3, 2, 1],[-3, 1, 2],
   [ 1,-2, 3],[ 1,-3, 2],[ 2,-1, 3],[ 2,-3, 1],[ 3,-2, 1],[ 3,-1, 2],
   [ 1, 2,-3],[ 1, 3,-2],[ 2, 1,-3],[ 2, 3,-1],[ 3, 2,-1],[ 3, 1,-2],
   [-1,-2, 3],[-1,-3, 2],[-2,-1, 3],[-2,-3, 1],[-3,-2, 1],[-3,-1, 2],
   [-1, 2,-3],[-1, 3,-2],[-2, 1,-3],[-2, 3,-1],[-3, 2,-1],[-3, 1,-2],
   [ 1,-2,-3],[ 1,-3,-2],[ 2,-1,-3],[ 2,-3,-1],[ 3,-2,-1],[ 3,-1,-2],
   [-1,-2,-3],[-1,-3,-2],[-2,-1,-3],[-2,-3,-1],[-3,-2,-1],[-3,-1,-2],
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

def get_scanner_locations(pair0, pair1, rotations):
    # given two pair of beacons that we know map to each other, find
    # translations/rotations that map pair1 to pair0
    # return: list of (rotation,translation) pairs;
    # (pair0 should always be scanner0)
    retval = []
    s0b0,s0b1 = pair0;
    s1b0,s1b1 = pair1;

    found = False;

    logger.debug(f"get_scanner_location checking pairs ({s0b0},{s0b1}) ({s1b0},{s1b1})");
    # try all rotations, calculate translation, verify translation is the same
    # for both points; if so, we've found the right rotation/translation
    for rotation in rotations:
        rotated_s1b0 = rotate(s1b0, rotation);
        rotated_s1b1 = rotate(s1b1, rotation);
        #logger.debug(f"                            rotation {rotation}");
        #logger.debug(f"                              rotated pair1 ({rotated_s1b0},{rotated_s1b1})");

        translation = [rotated_s1b0[i] - s0b0[i] for i in range(len(s0b0))];
        logger.debug(f"                              translation0 ({translation}) gives {translate(rotated_s1b1, translation)} to match {s0b1}");
        if translate(rotated_s1b1, translation) == list(s0b1):
            retval.append((rotation, translation));

        translation = [rotated_s1b1[i] - s0b0[i] for i in range(len(s0b0))];
        logger.debug(f"                              translation1 ({translation}) gives {translate(rotated_s1b0, translation)} to match {s0b1}");
        if translate(rotated_s1b0, translation) == list(s0b1):
            logger.debug(f"   found matching rotation {rotation} translation "\
                    f" {translation}");
            retval.append((rotation, translation));
    logger.debug(f"    returning {retval}");
    return retval;


class scanner():
    def __init__(self, fh, name = None, beacons = None, rotations = ROTATIONS,
            location = None):
        self.mapped = False;
        self.ntries = 0;
        self.rotations = rotations;
        self.beacon_distances = {};
        self.scanner_locations = [];
        if location is not None:
            self.scanner_locations.append(location);

        # read title line
        if name:
            self.name = name;
        else:
            self.name = str(scanf.scanf('--- scanner %d ---'));
        # read beacons
        self.beacons = [];
        if beacons:
            for b in beacons:
                self.add_beacon(b);
        else:
            self.beacons = [];
            scanf_retval = scanf.scanf('%d,%d,%d');
            while(scanf_retval):
                self.add_beacon(scanf_retval);
                scanf_retval = scanf.scanf('%d,%d,%d');
        if len(self.beacons) > 0:
            self.scanner_locations.append([0] * len(self.beacons[0]));

    def add_scanner_location(self, location):
        # add a new scanner location to the list of scanner locations this
        # scanner covers
        self.scanner_locations.append(location);

    def add_beacon(self, beacon):
        beacon = tuple(beacon);
        if not beacon in self.beacons:
            for b in self.beacons:
                self.beacon_distances[distance_squared(beacon, b)] = (beacon, b);
            self.beacons.append(beacon);

    def check_rotation_translation(self, other, rotation, translation, logger):
        # check all beacons in the other scanner. If they either
        # rotate/translate to here, or are out of range, we're good.
        found = 0;
        logger.debug(f"... checking {other.name} location "\
                f"{translate(rotate([0,0,0], rotation),translation)}" \
                f" r{rotation} t{translation}");
        for b in other.beacons:
            moved = tuple(translate(rotate(b, rotation), translation));
            logger.debug(f"... {b} -> {moved}");
            # if the translated beacon is either in our list of beacons, or out
            # of range of all our scanners, it's fine
            # so we check the converse: is the beacon not in our list of
            # beacons? is it in range of any of our scanners? If so, problem!
            if moved in self.beacons:
                logger.debug(f"Found {b} -> {moved}");
                found += 1;
            else:
                logger.debug(f".... {moved} not in self.beacons");
                # not in self.beacons; verify this beacon is out of range
                isinrange = False
                if inrange(moved, self.scanner_locations):
                    logger.debug(f"....  {other.name} beacon {b} r{rotation} t{translation} -> {moved} not in {self.name} but in range of {self.scanner_locations}");
                    return False;
                else:
                    logger.debug(f"....  {moved} out of range");
        logger.debug(f"  {other.name} r{rotation} t{translation} verified {found} matches!");
        # we know 2 will match, that's how we derived this
        # rotation/translation. We need at least one more beacon to match up.
        if found > 2:
            logger.debug(f"   verified matching rotation {rotation}" \
                    f" translation {translation}");
        return found > 2;

    def find_overlap(self, other, logger):
        logger.debug(f"Finding overlap between {self.name} and {other.name}");
        #logger.debug(f"  self.distances : " + ",".join([str(x) for x in self.beacon_distances.keys()]));
        #logger.debug(f"  other.distances: " + ",".join([str(x) for x in other.beacon_distances.keys()]));
        for distance in self.beacon_distances:
            if distance in other.beacon_distances:
                logger.debug(f"    found matching distance {distance} between"\
                        f" {self.beacon_distances[distance]}" \
                        f" and {other.beacon_distances[distance]}");
                possible_locations = get_scanner_locations(
                        self.beacon_distances[distance],
                        other.beacon_distances[distance],
                        self.rotations);
                for rotation,translation in possible_locations:
                    # rotate/translate other beacons, check for match
                    if self.check_rotation_translation(other, rotation,
                            translation, logger): return (rotation,
                                    translation);


def coalesce_beacons(scanners, logger, scannerrange = 1000):
    # calculate translation, translate all beacons, put locations of all
    # beacons relative to the first scanner in our dictionary of beacons
    scanner0 = scanners.pop(0);
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
        logger.debug(f"     " + "\n     ".join([str(b) for b in scanner0.beacons]));
        answer = scanner0.find_overlap(s, logger);
        if answer is not None:
            rotation, translation = answer
            new_scanner_location = translate(rotate([0,0,0], rotation),
                    translation);
            scanner0.add_scanner_location(new_scanner_location);
            for b in s.beacons:
                scanner0.add_beacon(translate(rotate(b, rotation),
                    translation));
            logger.debug(f"adding {len(s.beacons)} from {s.name} at" \
                    f" {new_scanner_location}");
        else:
            # could not find location of this scanner. Try again later.
            s.ntries += 1;
            if s.ntries >= max_ntries:
                raise Exception(f"Scanner {s.name}: maxed out overlap" \
                        f" attempts.  Scanner list: {scanner0.scanner_locations}");
            scanners.append(s);

    # part 2
    max_dist = 0;
    for idx, s0 in enumerate(scanner0.scanner_locations):
        for s1 in scanner0.scanner_locations[idx+1:]:
            new_dist = abs(s0[0] - s1[0]) + \
                    abs(s0[1] - s1[1]) + abs(s0[2] - s1[2]);
            max_dist = max(max_dist, new_dist);

    print(f"maximum Manhattan distance: {max_dist}");

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
            if(tuple(rotated) != s.beacons[beacon_idx]):
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
                [-485,-357,347],], location = [0,0,0]);
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
    correct_rotation = [-1, 2, -3];
    translation = [-68,1246,43];
    answer0 = translate(rotate(beacon1, correct_rotation), translation);
    expected0 = [-618,-824,-621];
    if answer0 != expected0:
        print(f"  rotation {correct_rotation} translation {translation} of {beacon1}" \
                f" produced {answer0}, expected {expected0}")
        nerrs += 1;
    answer1 = translate(rotate(rotation_translation_test_scanner2.beacons[1], correct_rotation), translation)
    expected1 = [-537,-823,-458];
    if answer1 != expected1:
        print(f"  rotation {correct_rotation} translation {translation} of" \
                " {rotation_translation_test_scanner2.beacons[1]}" \
                f" produced {answer0}, expected {expected1}")
        nerrs += 1;

    rotated = rotate(beacon1, correct_rotation);
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
    logger.debug(f"#### known pair test. Rotation {correct_rotation} translation {calc_translation}.");
    answer = get_scanner_locations(
            (rotation_translation_test_scanner.beacons[0],
             rotation_translation_test_scanner.beacons[1]),
            (rotation_translation_test_scanner2.beacons[0],
             rotation_translation_test_scanner2.beacons[1]),
            ROTATIONS);
    if answer is None:
        print(f"ERROR: didn't find scanner0/scanner1 first pair rotation/translation");
        nerrs += 1;
    else:
        rotation, translation = answer[1]
        expected_rotation = [-1, 2, -3];
        if(expected_rotation != rotation):
            print(f"ERROR: unexpected rotation {rotation} calculated from" \
                    f" scanner0/1 first pair. Expected {expected_rotation}");
            nerrs += 1;
        expected_translation = [-68,1246,43];
        if(expected_translation != translation):
            print(f"ERROR: unexpected translation {translation} calculated,"
                    f" expected {expected_translation}");
            nerrs += 1;

    answer = rotation_translation_test_scanner.find_overlap(
            rotation_translation_test_scanner2, logger);
    if answer is None:
        print(f"ERROR: didn't find scanner2 rotation/translation");
        nerrs += 1;
    else:
        rotation, translation = answer
        expected_rotation = [-1, 2, -3];
        if(expected_rotation != rotation):
            print(f"ERROR: unexpected rotation {rotation} calculated, expected " \
                    f"{expected_rotation}");
            nerrs += 1;
        expected_translation = (-68,1246,43);
        if(expected_translation != tuple(translation)):
            print(f"ERROR: unexpected translation {translation} calculated, expected " \
                    f"{expected_translation}");
            nerrs += 1;

    print(f"{nerrs} errors");

    '''
    tr = [-1,2,-3];
    tt=[-68,1246,43];
    testrt = [([-1,2,-3],[-68,1246,43]),
              ([-1,2,-3],[-68,-1246,43])];
    for tr, tt in testrt:
        print(f"----- r{tr} t{tt}");
        for b in rotation_translation_test_scanner2.beacons:
            print(f"{b} -> {translate(rotate(b, tr), tt)}");
    '''

    '''
    found matching distance 25910 between ((2059, 636, 411), (1969, 749, 482)) and ((450, -373, -389), (563, -302, -299))     
    '''

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

