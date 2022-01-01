import sys;
import logging;
import copy;

AOC_DAY=23
AOC_YEAR=2021


'''
#############
#...........#
###D#B#C#A###
  #D#C#B#A#
  #D#B#A#C#
  #C#A#D#B#
  #########

positions:
 # p q  r s  t u  v w  x y z #
 # # # a3 # b3 # c3 # d3 # # #
     # a2 # b2 # c2 # d2 #
     # a1 # b1 # c1 # d1 #
     # a0 # b0 # c0 # d0 #

'''
amphipod_cost = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
}

movement_paths = {
        ('a0','p'):['a1','a2','a3','r','q'],
        ('a1','p'):['a2','a3','r','q'],
        ('a2','p'):['a3','r','q'],
        ('a3','p'):['r','q'],
        ('b0','p'):['b1','b2','b3','t','s','r','q'],
        ('b1','p'):['b2','b3','t','s','r','q'],
        ('b2','p'):['b3','t','s','r','q'],
        ('b3','p'):['t','s','r','q'],
        ('c0','p'):['c1','c2','c3','v','u','t','s','r','q'],
        ('c1','p'):['c2','c3','v','u','t','s','r','q'],
        ('c2','p'):['c3','v','u','t','s','r','q'],
        ('c3','p'):['v','u','t','s','r','q'],
        ('d0','p'):['d1','d2','d3','x','w','v','u','t','s','r','q'],
        ('d1','p'):['d2','d3','x','w','v','u','t','s','r','q'],
        ('d2','p'):['d3','x','w','v','u','t','s','r','q'],
        ('d3','p'):['x','w','v','u','t','s','r','q'],

        ('a0','q'):['a1','a2','a3','r'],
        ('a1','q'):['a2','a3','r'],
        ('a2','q'):['a3','r'],
        ('a3','q'):['r'],
        ('b0','q'):['b1','b2','b3','t','s','r'],
        ('b1','q'):['b2','b3','t','s','r'],
        ('b2','q'):['b3','t','s','r'],
        ('b3','q'):['t','s','r'],
        ('c0','q'):['c1','c2','c3','v','u','t','s','r'],
        ('c1','q'):['c2','c3','v','u','t','s','r'],
        ('c2','q'):['c3','v','u','t','s','r'],
        ('c3','q'):['v','u','t','s','r'],
        ('d0','q'):['d1','d2','d3','x','w','v','u','t','s','r'],
        ('d1','q'):['d2','d3','x','w','v','u','t','s','r'],
        ('d2','q'):['d3','x','w','v','u','t','s','r'],
        ('d3','q'):['x','w','v','u','t','s','r'],

        ('a0','s'):['a1','a2','a3','r'],
        ('a1','s'):['a2','a3','r'],
        ('a2','s'):['a3','r'],
        ('a3','s'):['r'],
        ('b0','s'):['b1','b2','b3','t'],
        ('b1','s'):['b2','b3','t'],
        ('b2','s'):['b3','t'],
        ('b3','s'):['t'],
        ('c0','s'):['c1','c2','c3','v','u','t'],
        ('c1','s'):['c2','c3','v','u','t'],
        ('c2','s'):['c3','v','u','t'],
        ('c3','s'):['v','u','t'],
        ('d0','s'):['d1','d2','d3','x','w','v','u','t'],
        ('d1','s'):['d2','d3','x','w','v','u','t'],
        ('d2','s'):['d3','x','w','v','u','t'],
        ('d3','s'):['x','w','v','u','t'],

        ('a0','u'):['a1','a2','a3','r','s','t'],
        ('a1','u'):['a2','a3','r','s','t'],
        ('a2','u'):['a3','r','s','t'],
        ('a3','u'):['r','s','t'],
        ('b0','u'):['b1','b2','b3','t'],
        ('b1','u'):['b2','b3','t'],
        ('b2','u'):['b3','t'],
        ('b3','u'):['t'],
        ('c0','u'):['c1','c2','c3','v'],
        ('c1','u'):['c2','c3','v'],
        ('c2','u'):['c3','v'],
        ('c3','u'):['v'],
        ('d0','u'):['d1','d2','d3','x','w','v'],
        ('d1','u'):['d2','d3','x','w','v'],
        ('d2','u'):['d3','x','w','v'],
        ('d3','u'):['x','w','v'],

        ('a0','w'):['a1','a2','a3','r','s','t','u','v'],
        ('a1','w'):['a2','a3','r','s','t','u','v'],
        ('a2','w'):['a3','r','s','t','u','v'],
        ('a3','w'):['r','s','t','u','v'],
        ('b0','w'):['b1','b2','b3','t','u','v'],
        ('b1','w'):['b2','b3','t','u','v'],
        ('b2','w'):['b3','t','u','v'],
        ('b3','w'):['t','u','v'],
        ('c0','w'):['c1','c2','c3','v'],
        ('c1','w'):['c2','c3','v'],
        ('c2','w'):['c3','v'],
        ('c3','w'):['v'],
        ('d0','w'):['d1','d2','d3','x'],
        ('d1','w'):['d2','d3','x'],
        ('d2','w'):['d3','x'],
        ('d3','w'):['x'],

        ('a0','y'):['a1','a2','a3','r','s','t','u','v','w','x'],
        ('a1','y'):['a2','a3','r','s','t','u','v','w','x'],
        ('a2','y'):['a3','r','s','t','u','v','w','x'],
        ('a3','y'):['r','s','t','u','v','w','x'],
        ('b0','y'):['b1','b2','b3','t','u','v','w','x'],
        ('b1','y'):['b2','b3','t','u','v','w','x'],
        ('b2','y'):['b3','t','u','v','w','x'],
        ('b3','y'):['t','u','v','w','x'],
        ('c0','y'):['c1','c2','c3','v','w','x'],
        ('c1','y'):['c2','c3','v','w','x'],
        ('c2','y'):['c3','v','w','x'],
        ('c3','y'):['v','w','x'],
        ('d0','y'):['d1','d2','d3','x'],
        ('d1','y'):['d2','d3','x'],
        ('d2','y'):['d3','x'],
        ('d3','y'):['x'],

        ('a0','z'):['a1','a2','a3','r','s','t','u','v','w','x','y'],
        ('a1','z'):['a2','a3','r','s','t','u','v','w','x','y'],
        ('a2','z'):['a3','r','s','t','u','v','w','x','y'],
        ('a3','z'):['r','s','t','u','v','w','x','y'],
        ('b0','z'):['b1','b2','b3','t','u','v','w','x','y'],
        ('b1','z'):['b2','b3','t','u','v','w','x','y'],
        ('b2','z'):['b3','t','u','v','w','x','y'],
        ('b3','z'):['t','u','v','w','x','y'],
        ('c0','z'):['c1','c2','c3','v','w','x','y'],
        ('c1','z'):['c2','c3','v','w','x','y'],
        ('c2','z'):['c3','v','w','x','y'],
        ('c3','z'):['v','w','x','y'],
        ('d0','z'):['d1','d2','d3','x','y'],
        ('d1','z'):['d2','d3','x','y'],
        ('d2','z'):['d3','x','y'],
        ('d3','z'):['x','y','y'],
}

def cost(start, end, amphipod):
    if start[0] in ['a','b','c','d']:
        return (len(movement_paths[(start, end)]) + 1) * amphipod_cost[amphipod[0]];
    else:
        return (len(movement_paths[(end, start)]) + 1) * amphipod_cost[amphipod[0]];

# return None if amphipod can't move any more
def get_all_next_moves(start, amphipod, board):
    # check to see if we're moving an amphipod which is already in a final slot
    if start[0] == amphipod[0].lower():
        finalspot = True;
        for i in range(0, int(start[1])):
            checkspot = start[0] + str(i);
            if board.get(checkspot, 'e')[0] != checkspot[0].upper():
                # found an amphipod not in a final spot who'd be blocked in
                finalspot = False;
                break;
        if finalspot:
            return [];

    if start[0] in ['a','b','c','d']:
        return ['p','q','s','u','w','y','z'];
    else:
        endspot = amphipod[0].lower();
        return [endspot + str(x) for x in range(0, 4)]

def is_legal_move(start, end, board):
    # check to see if end is occupied
    if end in board:
        return False;

    # check to see if any spot along the move path is occupied
    if start[0] in ['a','b','c','d']:
        path = movement_paths[(start, end)]
    else:
        path = movement_paths[(end, start)]
    for step in path:
        if step in board:
            return False

    # check to see if we're moving an amphipod into a final slot which will
    # block other amphipods from getting out, or if we're moving into a spot
    # that will block an empty spot
    if end[0] in ['a','b','c','d']:
        for i in range(0, int(end[1])):
            checkspot = end[0] + str(i);
            if not checkspot in board:
                # this move would block an empty spot
                return False;
            if not board[checkspot][0] == checkspot[0].upper():
                # this move would block an amphipod in
                return False;

    return True;

# return True if all amphipods are in the right side rooms
def check_done(board):
    for (room, amphipod) in board.items():
        if room[0] != amphipod[0].lower():
            return False;

    return True;


def create_start_board(test = False):
    if(test):
        board = {
                'a3':'B0',
                'a2':'D0',
                'a1':'D1',
                'a0':'A0',
                'b3':'C0',
                'b2':'C1',
                'b1':'B1',
                'b0':'D2',
                'c3':'B2',
                'c2':'B3',
                'c1':'A1',
                'c0':'C2',
                'd3':'D3',
                'd2':'A2',
                'd1':'C3',
                'd0':'A3',
        }
    else:
        board = {
                'a3':'D0',
                'a2':'D1',
                'a1':'D3',
                'a0':'C0',
                'b3':'B0',
                'b2':'C1',
                'b1':'B1',
                'b0':'A0',
                'c3':'C2',
                'c2':'B2',
                'c1':'A1',
                'c0':'D3',
                'd3':'A2',
                'd2':'A3',
                'd1':'C3',
                'd0':'B3',
        }

    return board;

def board_repr(board):
    return f"# {board.get('p', '. ')} {board.get('q', '. ')} .  " \
            f"{board.get('s', '. ')} .  {board.get('u', '. ')} .  " \
            f"{board.get('w', '. ')} .  {board.get('y', '. ')} " \
            f"{board.get('z', '. ')} #\n" \
            f"     #  {board.get('a3', '. ')} ## {board.get('b3', '. ')} ## " \
            f"{board.get('c3', '. ')} ## {board.get('d3', '. ')} #\n" \
            f"     #  {board.get('a2', '. ')} ## {board.get('b2', '. ')} ## " \
            f"{board.get('c2', '. ')} ## {board.get('d2', '. ')} #\n" \
            f"     #  {board.get('a1', '. ')} ## {board.get('b1', '. ')} ## " \
            f"{board.get('c1', '. ')} ## {board.get('d1', '. ')} #\n" \
            f"     #  {board.get('a0', '. ')} ## {board.get('b0', '. ')} ## " \
            f"{board.get('c0', '. ')} ## {board.get('d0', '. ')} #\n"

def find_lowest_energy(board):
    # plan: complete search of all possible moves
    # find all possible moves by all possible amphipods
    #  store "board" for each
    lowest_energy = None;
    boardlist = [(board, 0, [])];
    nrounds = 0;
    checked_boards = {};
    while len(boardlist) > 0:
        board, current_cost, movelist = boardlist.pop();
        if (board_repr(board), current_cost) in checked_boards:
            # we're already checking this board
            continue;

        if(current_cost > (1000*4 + 100*4 + 10*4 + 1*4) * 22):
            print(f"WARNING: discarding board, cost {current_cost} greater than max");
            print(board_repr(board));
            print(movelist);
            continue;

        checked_boards[(board_repr(board), current_cost)] = 1;
        if lowest_energy != None and (current_cost >= lowest_energy):
            continue;
        # generate all possible next moves on this board
        logger.debug(board_repr(board));
        for(position, amphipod) in board.items():
            nextmoves = get_all_next_moves(position, amphipod, board);
            logger.debug(f"checking {amphipod} from {position} to {nextmoves}");
            if None != nextmoves:
                for nextmove in nextmoves:
                    if is_legal_move(position, nextmove, board):
                        nextboard = copy.deepcopy(board)
                        nextboard.pop(position);
                        nextboard[nextmove] = amphipod;
                        nextcost = current_cost + cost(position, nextmove, amphipod);
                        logger.debug(f"-- amphipod {amphipod} moves {position}-{nextmove}, cost now {nextcost}");
                        if check_done(nextboard):
                            logger.debug(f"finished board! Energy {nextcost} (current min {lowest_energy})");
                            if None == lowest_energy:
                                lowest_energy = nextcost;
                            else:
                                lowest_energy = min(lowest_energy, nextcost);
                        else:
                            boardlist.append((nextboard, nextcost, movelist + [(amphipod, position, nextmove)]));
        nrounds += 1;
        if 0 == nrounds % 10000:
            print(f"Round {nrounds}, minimum cost {lowest_energy} (board cost {current_cost})");
            print(board_repr(board));

    return lowest_energy;


if('__main__' == __name__):
    import argparse;

    # deal with command line arguments
    parser = argparse.ArgumentParser(
            description = 'Advent of Code {} day {} solution'.format(
                AOC_YEAR, AOC_DAY));
    logger = logging.Logger('AOC{}d{}'.format(AOC_YEAR, AOC_DAY));
    logger.addHandler(logging.StreamHandler());

    parser.add_argument(
        '-T', '--test', action='store_true',
        help='test', default=False);
    parser.add_argument(
        '-2', '--part2', action='store_true',
        help='part 2?', default=False);
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='be verbose', default=False);

    args = parser.parse_args();
    if(args.verbose):
        logger.setLevel(logging.DEBUG);
    else:
        logger.setLevel(logging.INFO);

    board = create_start_board(args.test);
    lowest_energy = find_lowest_energy(board);

    print(f"Lowest energy: {lowest_energy}");

