import sys;
import logging;
import heapq;

AOC_DAY=15
AOC_YEAR=2021


class riskgrid_element():
    def __init__(self, weight, coords):
        self.weight = int(weight);
        self.x = coords[0]
        self.y = coords[1]
        self.visited = False;
        self.distance = 0;
    def visit(self):
        old_visited = self.visited;
        self.visited = True;
        return old_visited;
    def __lt__(self, other):
        return self.distance < other.distance;
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y);
    def get_neighbors(self, width, height):
        retval = [];
        if(self.x > 0):
            retval.append((self.x-1, self.y));
        if(self.y > 0):
            retval.append((self.x, self.y-1));
        if(self.x < width - 1):
            retval.append((self.x+1, self.y));
        if(self.y < height - 1):
            retval.append((self.x, self.y+1));
        return retval;
    def get_neighbors_with_diagonal(self, width, height):
        retval = [];
        if self.x > 0:
            if self.y > 0:
                retval.append((self.x-1, self.y-1));
            retval.append((self.x-1, self.y));
            if self.y < height - 1:
                retval.append((self.x-1, self.y+1));
        if self.y > 0:
            retval.append((self.x, self.y-1));
        if self.y < height - 1:
            retval.append((self.x, self.y+1));
        if self.x < width - 1:
            if self.y > 0:
                retval.append((self.x+1, self.y-1));
            retval.append((self.x+1, self.y));
            if self.y < height - 1:
                retval.append((self.x+1, self.y+1));
        
        return retval;

def test_riskgrid(logger):
    nerrs = 0;

    # damn diagonals
    testcases = [
            ((0,0), 5, 5, [(0,1), (1,0), (1,1)]),
            ((1,0), 5, 5, [(0,0), (0,1), (1,1), (2,0), (2,1)]),
            ((0,1), 5, 5, [(0,0), (0,2), (1,0), (1,1), (1,2)]),
            ((1,1), 5, 5, [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]),
            ((4,4), 5, 5, [(3,3), (3,4), (4,3)]),
            ((4,3), 5, 5, [(3,2), (3,3), (3,4), (4,2), (4,4)]),
            ((3,4), 5, 5, [(2,3), (2,4), (3,3), (4,3), (4,4)]),
            ((3,3), 5, 5, [(2,2), (2,3), (2,4), (3,2), (3,4), (4,2), (4,3), (4,4)]),
            ];
    testcases = [
            ((0,0), 5, 5, [(1,0), (0,1)]),
            ((1,0), 5, 5, [(0,0), (2,0), (1,1)]),
            ((0,1), 5, 5, [(0,0), (1,1), (0,2)]),
            ((1,1), 5, 5, [(0,1), (1,0), (2,1), (1,2)]),
            ((4,4), 5, 5, [(3,4), (4,3)]),
            ((4,3), 5, 5, [(3,3), (4,2), (4,4)]),
            ((3,4), 5, 5, [(2,4), (3,3), (4,4)]),
            ((3,3), 5, 5, [(2,3), (3,2), (4,3), (3,4)]),
            ];
    for coords, width, height, answer in testcases:
        ge = riskgrid_element(1, coords);
        calc_answer = ge.get_neighbors( width, height);
        if(answer != calc_answer):
            print(f"ERROR: testcase {coords} calculated:\n    {calc_answer}\n  expected:\n    {answer}");
        nerrs += 1;
    return nerrs;


def read_riskgrid(part2 = False):
    # note: grid access is grid[y][x]
    weights = [[x for x in line.strip()] for line in sys.stdin.readlines()];
    grid = [[riskgrid_element(weights[x][y], (x,y)) for y in range(len(weights))] for x in range(len(weights[0]))]

    if part2:
        # expand grid
        width = len(grid[0]);
        height = len(grid);
        for y in range(height):
            for x in range(width, 5 * width):
                grid[y].append(riskgrid_element(
                    ((int(weights[y][x % width]) + (x // width) - 1) % 9) + 1, (x,y)))
        for y in range(height, height * 5):
            grid.append([]);
            for x in range(5 * width):
                grid[y].append(riskgrid_element(
                    ((int(weights[y % height][x % width]) + (x//width) + (y//height) - 1) % 9) + 1, (x,y)))

    return grid;

def riskgrid_repr(grid):
    return '\n'.join([''.join([str(x.weight) for x in y]) for y in grid]);

#g = read_riskgrid(True)
#print(riskgrid_repr(g));
#sys.exit(1);


def djikstra(grid, logger):
    # priority queue
    # start with only the start element in the priority queue
    q = [grid[0][0]];
    width = len(grid[0]);
    height = len(grid);

    end_coords = (len(grid) - 1, len(grid[0]) - 1)
    # pop element with lowest distance
    popped = heapq.heappop(q);
    # on each step:
    while (popped.x, popped.y) != end_coords:
        logger.debug(f"Visiting ({popped.x},{popped.y}) dist {popped.distance}");
        # if not visited
        if not popped.visited:
            popped.visit();
            # for each neighbor:
            neighbors = popped.get_neighbors(width, height);
            for neighbor in [grid[neighbor[1]][neighbor[0]] for neighbor in neighbors]:
                # if not visited
                if not neighbor.visited:
                    # calculate new distance, and put on heap
                    neighbor.distance = min(popped.distance + neighbor.weight,
                            max(neighbor.distance, popped.distance + neighbor.weight));
                    logger.debug(f"  queuing neighbor ({neighbor.x},{neighbor.y})" \
                            f" weight {neighbor.weight}  dist {neighbor.distance}");
                    logger.debug(f"    min({popped.distance}+{neighbor.weight}," \
                            f" max({neighbor.distance}, {popped.distance} + {neighbor.weight}))");
                    heapq.heappush(q, neighbor);

        # pop next least-cost element
        popped = heapq.heappop(q);

    return popped.distance


def test(logger):
    nerrs = 0;
    nerrs += test_riskgrid(logger);
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
        help='unit test', default=False);

    args = parser.parse_args();
    if(args.verbose):
        logger.setLevel(logging.DEBUG);
    if(args.test):
        nerrs = test(logger);
        sys.exit(nerrs);

    g = read_riskgrid(args.part2);
    logger.debug("Initial grid:\n{}".format(riskgrid_repr(g)));

    lowest_risk = djikstra(g, logger);
    print(f"Lowest risk path: {lowest_risk}");

