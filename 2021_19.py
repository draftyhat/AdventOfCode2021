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
      x, y, z   y, x, z   z, y, x   y, z, x
     -x, y, z  -y, x, z  -z, y, x  -y, z, x
      x,-y, z   y,-x, z   z,-y, x   y,-z, x
      x, y,-z   y, x,-z   z, y,-x   y, z,-x
     -x,-y, z  -y,-x, z  -z,-y, x  -y,-z, x
     -x, y,-z  -y, x,-z  -z, y,-x  -y, z,-x
      x,-y,-z   y,-x,-z   z,-y,-x   y,-z,-x
     -x,-y,-z  -y,-x,-z  -z,-y,-x  -y,-z,-x
'''

AOC_DAY=19
AOC_YEAR=2021

ROTATIONS=[
   [  1, 2, 3 ],[  2, 1, 3 ],[  3, 2, 1 ],[  2, 3, 1 ],
   [ -1, 2, 3 ],[ -2, 1, 3 ],[ -3, 2, 1 ],[ -2, 3, 1 ],
   [  1,-2, 3 ],[  2,-1, 3 ],[  3,-2, 1 ],[  2,-3, 1 ],
   [  1, 2,-3 ],[  2, 1,-3 ],[  3, 2,-1 ],[  2, 3,-1 ],
   [ -1,-2, 3 ],[ -2,-1, 3 ],[ -3,-2, 1 ],[ -2,-3, 1 ],
   [ -1, 2,-3 ],[ -2, 1,-3 ],[ -3, 2,-1 ],[ -2, 3,-1 ],
   [  1,-2,-3 ],[  2,-1,-3 ],[  3,-2,-1 ],[  2,-3,-1 ],
   [ -1,-2,-3 ],[ -2,-1,-3 ],[ -3,-2,-1 ],[ -2,-3,-1 ],
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
            self.beacons = beacons;
        else:
            self.beacons = [];
            scanf_retval = scanf.scanf('%d,%d,%d');
            while(scanf_retval):
                self.beacons.append(list(scanf_retval));
                scanf_retval = scanf.scanf('%d,%d,%d');

    def find_offset(self, beacons, scanners, logger, scannerrange = 1000):
        # find where this scanner is located relative to the given list of
        # beacons
        for selfbeacon in self.beacons:
            logger.debug(f"- start selfbeacon loop: selfbeacon{selfbeacon}");
            for otherbeacon_original in beacons:
                otherbeacon = list(otherbeacon_original);
                logger.debug(f"-- start otherbeacon loop: otherbeacon{otherbeacon}");
                match = None;
                for rotation in self.rotations:
                    logger.debug(f"--- start rotation loop {selfbeacon} - {otherbeacon} rotation {rotation}");
                    match = None
                    # assume these are the same beacon under some translation
                    # and the chosen rotation.
                    # rotate the other beacon
                    rotated = rotate(selfbeacon, rotation);
                    logger.debug(f"    {selfbeacon} rotated: {rotated}");

                    # find the translation between the two beacons.
                    translation = [rotated[i] - otherbeacon[i] for i in \
                            range(len(rotated))];
                    logger.debug(f"    translation: {translation}  about to" \
                            f" check {len(self.beacons)} beacons");

                    # apply this translation and rotation to other self beacons
                    otherbeacons = copy.deepcopy(beacons);
                    otherbeacons.remove(otherbeacon_original);
                    for checkbeacon in self.beacons:
                        if(checkbeacon == selfbeacon):
                            continue;
                        moved_checkbeacon = rotate(checkbeacon, rotation);
                        moved_checkbeacon = translate(moved_checkbeacon, translation);
                        logger.debug(f"       ---- check loop checking {checkbeacon}, rotated to {rotate(checkbeacon, rotation)}, translated to {moved_checkbeacon}");
                        if moved_checkbeacon == [534,-1912,768]:
                            logger.debug('  !!!!!!!!!!!!!!!!!!!!!!!!\n  check beacon ' + '\n  check beacon'.join([str(b) for b in otherbeacons]));
                        if(inrange(moved_checkbeacon, scanners, scannerrange)):
                            # coerce type
                            if type(moved_checkbeacon) != type(otherbeacon_original):
                                moved_checkbeacon = type(otherbeacon_original)(moved_checkbeacon);
                            # see if the calculated beacon is in the check list
                            if not moved_checkbeacon in otherbeacons:
                                logger.debug(f"--- found non-matching beacon {moved_checkbeacon} ({checkbeacon})")
                                match = False;
                                break;
                            # found beacon
                            otherbeacons.remove(moved_checkbeacon);
                            match = True;
                        else:
                            logger.debug(f"moved beacon {checkbeacon}->{moved_checkbeacon} out of range");
                        if(match):
                            # apply the last translation and rotation to
                            # leftover other beacons; verify they're all out of
                            # range of this scanner.
                            for leftover_otherbeacon in otherbeacons:
                                moved = rotate_inverse(translate(leftover_otherbeacon,
                                    [-x for x in translation]),
                                    rotation);
                                if inrange(moved, scanners, scannerrange):
                                    logger.debug(f"  leftover_otherbeacon {leftover_otherbeacon} " \
                                            f" -> {moved} is in range of scanner" \
                                            f" but not found in list. Failing"
                                            f" this match.");
                                    match = False;
                                    break;

                        logger.debug(f"    end loop, match {match}");
                        if(match):
                            return(rotation, translation);
                    logger.debug(f"    end rotation loop");
                logger.debug(f"    end otherbeacon loop");
            logger.debug(f"    end selfbeacon loop");
        # no match found
        return None;

def coalesce_beacons(scanners, scannerrange = 1000):
    # calculate translation, translate all beacons, put locations of all
    # beacons relative to the first scanner in our dictionary of beacons
    beacons = set();
    scanner0 = scanners.pop(0);
    scanner_location_list = [[0] * len(scanner0.beacons[0])];
    logger.debug(f"adding {len(scanner0.beacons)} from {scanner0.name} ({len(scanners)} scanners)");
    for b in scanner0.beacons:
        beacons.add(tuple(b));
    max_ntries = len(scanners);
    while len(scanners) > 0:
        s = scanners.pop(0);
        logger.debug(f"=========== checking scanner {s.name}");
        answer = s.find_offset(beacons,
                scanner_location_list, logger = logger, scannerrange = scannerrange);
        if None == answer:
            # this scanner didn't overlap. Try later.
            s.ntries += 1;
            if s.ntries > max_ntries:
                raise Exception(f"Scanner {s.name}: maxed out overlap" \
                        f" attempts.  Scanner list: {scanner_location_list}");
            scanners.append(s);
            continue;
        (rotation, translation) = answer;
        logger.debug(f"adding {len(s.beacons)} from {s.name}");
        scanner_location_list.append(negate(translation));
        for b in s.beacons:
            beacons.add(tuple(translate(rotate(b, rotation), translation)));
            logger.debug(f"  adding {tuple(translate(rotate(b, rotation), translation))}");
    return beacons;


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

    answer = rotation_translation_test_scanner2.find_offset(
            rotation_translation_test_scanner.beacons, [[0,0,0]], logger);
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

    beacons = coalesce_beacons(scanners, scannerrange = 10);
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
        nerrs += test2d(logger);
        nerrs += test_rotation(logger);
        sys.exit(nerrs);

    # read scanners/beacons
    scanners = []
    line = sys.stdin.readline();
    while(line):
        scanners.append(scanner(sys.stdin, name = line.strip()));
        line = sys.stdin.readline();

    beacons = coalesce_beacons(scanners);
    print(f"Found {len(beacons)} beacons");
    l = [str(x).strip('()') for x in beacons];
    l.sort();
    print('\n'.join(l));
