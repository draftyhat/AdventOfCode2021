import sys;
import logging;

AOC_DAY=15
AOC_YEAR=2021

class grid():
    def __init__(self, logger):
        self.grid = {};
        self.width = 0;
        self.height = 0;
        self.logger = logger;

    def traverse(self, x_start, y_start, x_end, y_end):
        # start at end. Calculate cost to get to all connected squares. Save
        # cost
        # if cost is less than previous cost, and if so, continue this path.
        to_traverse = {(x_end, y_end):1}
        (cost, ignore) = self.grid[(x_end, y_end)];
        self.grid[(x_end, y_end)] = (cost, 0);

        hash = 0;
        while(len(to_traverse) > 0):
            hash += 1;
            if(hash % 1000000 == 0):
                print(f"  step {hash}, {len(to_traverse)} to traverse");

            # pop the next location to check
            ((x, y), discard) = to_traverse.popitem();
            # go in every direction from this square
            (cost, cost_to_get_here) = self.grid[(x,y)];
            cost_to_get_here += cost;
            self.logger.debug(f"-- traversing ({x},{y}), pathcost {cost_to_get_here}");
            for (next_x, next_y) in [ (x+1,y),(x,y+1),(x-1,y),(x,y-1) ]:
                self.logger.debug(f" check ({next_x},{next_y})");
                if(next_x >= 0 and next_x < grid.width \
                        and next_y >= 0 and next_y < grid.height):
                    (next_cost, next_cost_to_get_here) = \
                            self.grid[(next_x, next_y)];
                    if -1 == next_cost_to_get_here or \
                            cost_to_get_here < next_cost_to_get_here:
                        self.grid[(next_x, next_y)] = (next_cost,
                                cost_to_get_here);
                        if (next_x, next_y) != (x_start, y_start):
                            to_traverse[ (next_x, next_y) ] = 1;

    def read(self):
        self.grid = {};
        line = sys.stdin.readline().strip();
        y = 0;
        while(len(line) > 0):
            for x, ch in enumerate(line):
                # grid[location] = (cost, cost_to_get_here)
                self.grid[(x, y)] = (int(ch), -1);
            y = y + 1;
            line = sys.stdin.readline().strip();
        self.width = x + 1;
        self.height = y;
        self.logger.debug(f" {self.width} x {self.height} grid");

    def __repr__(self):
        retval = ''
        for y in range(self.height):
            for x in range(self.width):
                retval += f"{self.grid[(x,y)][0]}";
            retval += '\n';
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

    grid = grid(logger);
    grid.read();
    grid.traverse(0, 0, grid.width - 1, grid.height - 1);
    (cost, pathcost) = grid.grid[(0,0)];
    print(f"Path cost: {pathcost}")

