import sys;
import logging;
import scanf;

AOC_DAY=5
AOC_YEAR=2021

def find_dangerous_vents(logger, part2 = False):
    vents = [];
    maxy = 0;
    # read in vector descriptions
    while True:
        try:
            (x1, y1, x2, y2) = scanf.scanf('%d,%d -> %d,%d');
            logger.debug("{},{} -> {},{}".format(x1, y1, x2, y2));

            if(x1 == x2):
                if(y1 < y2):
                    for y in range(y1, y2 + 1):
                        logger.debug("  Appending ({},{})".format(x1, y))
                        vents.append((x1, y));
                else:  # y2 > y1
                    for y in range(y2, y1 + 1):
                        logger.debug("  Appending ({},{})".format(x1, y))
                        vents.append((x1, y));
            elif(y1 == y2):
                if(x1 < x2):
                    for x in range(x1, x2 + 1):
                        logger.debug("  Appending ({},{})".format(x, y1))
                        vents.append((x, y1));
                else:
                    for x in range(x2, x1 + 1):
                        logger.debug("  Appending ({},{})".format(x, y1))
                        vents.append((x, y1));
            elif(part2):
                xstep = 1 if x1 < x2 else -1;
                ystep = 1 if y1 < y2 else -1;
                for increment in range((x2 - x1 + xstep) * xstep):
                    logger.debug("  Appending ({},{})".format(
                        x1 + xstep * increment, y1 + ystep * increment))
                    vents.append((x1 + xstep * increment,
                        y1 + ystep * increment));
            maxy = max(maxy, y1, y2)
        except Exception as e:
            logger.debug('quitting loop: {}'.format(e));
            break;

    # sort
    def keyfn(elt):
        return elt[0] * (maxy + 1) + elt[1];
    vents.sort(key=keyfn);

    logger.debug(vents);

    # find duplicates
    ndangerous = 0;
    nsame = 0;
    lastvent = vents[0]
    for vent in vents[1:]:
        if(lastvent == vent):
            logger.debug("Found sames {}".format(vent));
            nsame += 1;
        else:
            lastvent = vent;
            ndangerous += 1 if nsame > 0 else 0;
            nsame = 0;
    return ndangerous;

if('__main__' == __name__):
    import argparse;

    # deal with command line arguments
    parser = argparse.ArgumentParser(
            description = 'Advent of Code {} day {} solution'.format(
                AOC_YEAR, AOC_DAY));
    logger = logging.Logger('AOC{}d{}'.format(AOC_YEAR, AOC_DAY));
    logger.addHandler(logging.StreamHandler());

    parser.add_argument(
        '-2', '--part2', action='store_true',
        help='part 2?', default=False);
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='be verbose', default=False);

    args = parser.parse_args();
    if(args.verbose):
        logger.setLevel(logging.DEBUG);

    ndangerous = find_dangerous_vents(logger, part2 = args.part2);
    print(ndangerous);


