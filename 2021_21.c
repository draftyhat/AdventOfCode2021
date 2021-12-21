#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define AOC_YEAR 2021
#define AOC_DAY 21

#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define NPLAYERS 2
#define NROLLSPERTURN 3
#define NPOSITIONS 10

#ifdef TEST
#define PLAYER1START 4
#define PLAYER2START 8
#else
#define PLAYER1START 1
#define PLAYER2START 3
#endif

#ifdef PART2

/* notes on part 2:
 * - first check that test answers fit in an unsigned long. They do.
 * possible roll 1, 2, 3
 * 3 rolls each means possible turn position adds are:
 *  1 + 1 + 1 = 3
 *  1 + 1 + 2 = 4
 *  1 + 1 + 3 = 5
 *  1 + 2 + 1 = 4
 *  1 + 2 + 2 = 5
 *  1 + 2 + 3 = 6
 *  1 + 3 + 1 = 5
 *  1 + 3 + 2 = 6
 *  1 + 3 + 3 = 7
 *  2 + 1 + 1 = 4
 *  2 + 1 + 2 = 5
 *  2 + 1 + 3 = 6
 *  2 + 2 + 1 = 5
 *  2 + 2 + 2 = 6
 *  2 + 2 + 3 = 7
 *  2 + 3 + 1 = 6
 *  2 + 3 + 2 = 7
 *  2 + 3 + 3 = 8
 *  3 + 1 + 1 = 5
 *  3 + 1 + 2 = 6
 *  3 + 1 + 3 = 7
 *  3 + 2 + 1 = 6
 *  3 + 2 + 2 = 7
 *  3 + 2 + 3 = 8
 *  3 + 3 + 1 = 7
 *  3 + 3 + 2 = 8
 *  3 + 3 + 3 = 9
 *  so we can calculate the position increment after each turn:
 *     3 in 1 universe
 *     4 in 3 universes
 *     5 in 6 universes
 *     6 in 7 universes
 *     7 in 6 universes
 *     8 in 3 universes
 *     9 in 1 universes
 * in the universe where a player starts at position 1 and rolls all 1s, it'll
 * take him 7 turns to win. So games have at most 14 turns. At 3^3 = 27
 * possible universes per turn, that's (3 ^ 3)^14 = 109418989131512359209
 * possible universes. So we need to collapse the universes, we can't keep track
 * of each.
 * What if we keep track of the relative score? We still need to know when a
 * player wins, so that doesn't seem like it'll be enough.
 * There are 21 possible scores in a game, which means 21*21 possible game
 * scores on any one turn (that's fuzzy, there are actually many fewer, plus a
 * few because the score may go over 21). So the collection of all scores
 * should be trackable. But we'd need to track both scores and positions;
 * that's 21*21*10*10 = 44100 possible positions/scores at any single turn in
 * the game. That's a lot, but still trackable?
 */

#define WINNINGSCORE 7
#define MAXDIEVALUE 3

int main()
{
    int player1score, player2score, player1position, player2position;
    int position_increment, newscore;
    int turn;
    int alldone = 0;

    /* number of universes in which a game has a particular score and position,
     * indexed by [player1 score][player2 score][player1 position][player2
     * position] */
    unsigned long allgames[2][WINNINGSCORE][WINNINGSCORE][NPOSITIONS][NPOSITIONS];
    unsigned long player1wins = 0, player2wins = 0;
    unsigned long nuniverses;
    unsigned long new_nuniverses;

    /* number of universes which gain the index number of positions in a single
     * turn (see breakout above) */
    int position_increment_per_turn[10] = {
        0, 0, 0, 1, 3, 6, 7, 6, 3, 1 };
#define MINIMUM_POSITION_INCREMENT_PER_TURN 3
#define MAXIMUM_POSITION_INCREMENT_PER_TURN (sizeof(position_increment_per_turn)/sizeof(position_increment_per_turn[0]))

    memset(allgames, 0, sizeof(allgames));
    allgames[0][0][0][PLAYER1START - 1][PLAYER2START - 1] = 1;

    /* play out all games */
    while(!alldone)
    {
        DBGPRINT("-- starting turn %d\n", turn);
        /* zero out the spot where we'll keep the scores for the next turn */
        memset(allgames[(turn + 1) % 2], 0, sizeof(allgames[0]));
        alldone = 1;
        /* for each game we're tracking */
        for(player1score = 0; player1score < WINNINGSCORE; player1score++)
        {
            for(player2score = 0; player2score < WINNINGSCORE; player2score++)
            {
                for(player1position = 0; player1position < NPOSITIONS;
                        player1position++)
                {
                    for(player2position = 0; player2position < NPOSITIONS;
                            player2position++)
                    {
                        /* any games at this point? */
                        nuniverses = allgames[turn % 2][player1score][player2score][player1position][player2position];
                        DBGPRINT("--- p1 %d at %d, p2 %d at %d: %lu universes\n", player1score, player1position, player2score, player2position, nuniverses);
                        if(0 != nuniverses)
                        {
                            /* calculate range of possible games from here */
                            for(position_increment = MINIMUM_POSITION_INCREMENT_PER_TURN;
                                    position_increment < MAXIMUM_POSITION_INCREMENT_PER_TURN;
                                    position_increment++)
                            {
                                /* calculate number of new universes that will
                                 * have this score */
                                new_nuniverses = position_increment_per_turn[position_increment] * nuniverses;
                                /* calculate new score */
                                /* if player 1, add score to player 1, else add
                                 * to player 2 */
                                if(turn % 2)
                                {
                                    newscore = player1score +
                                        ((player1position + position_increment) % NPOSITIONS)
                                        + 1; /* positions index 0-9, position values 1-10 */
                                    /* mark wins */
                                    if(newscore >= WINNINGSCORE)
                                    {
                                        player1wins += new_nuniverses;
                                    }
                                    else
                                    {
                                        /* mark games at new score/position */
                                        allgames[(turn + 1) % 2]
                                            [(player1position + position_increment) % NPOSITIONS]
                                            [player2position]
                                            [newscore]
                                            [player2score] += new_nuniverses;
                                        alldone = 0;
                                    }
                                }
                                else /* player 2's turn */
                                {
                                    newscore = player2score +
                                        ((player2position + position_increment) % NPOSITIONS)
                                        + 1; /* positions index 0-9, position values 1-10 */
                                    if(newscore >= WINNINGSCORE)
                                        player2wins += new_nuniverses;
                                    else
                                    {
                                        /* mark games at new score/position */
                                        allgames[(turn + 1) % 2]
                                            [player1position]
                                            [(player2position + position_increment) % NPOSITIONS]
                                            [player1score]
                                            [newscore] += new_nuniverses;
                                        alldone = 0;
                                    }
                                }

                            }
                        }
                    }
                }
            }
        }
        turn++;
    }

    printf("Player 1 wins: %lu\n", player1wins);
    printf("Player 2 wins: %lu\n", player2wins);
}



#else /* part 1 */

#define WINNINGSCORE 1000

int main(int argc, char ** argv)
{
    int positions[NPLAYERS];
    unsigned long scores[NPLAYERS];
    int playerindex;
    unsigned long diceroll;
    int done;
    int turnroll;


    memset(scores, 0, sizeof(scores));
           
    positions[0] = PLAYER1START - 1;
    positions[1] = PLAYER2START - 1;

    /* on each iteration:
     *  increment player index modulo NPLAYERS
     *  roll die NROLLSPERTURN times
     *  move player around track
     *  add score to active player
     *  check for score above WINNINGSCORE
     */
    done = 0;
    diceroll = 1;
    for(playerindex = 0; !done; playerindex = (1 + playerindex) % NPLAYERS)
    {
        for(turnroll = 0; turnroll < NROLLSPERTURN; turnroll++, diceroll++)
        {
            positions[playerindex] =
                (positions[playerindex] + diceroll) % NPOSITIONS;
            DBGPRINT("-- player %d rolls %lu, moves to position %d\n",
                    playerindex, diceroll, positions[playerindex]);
        }
        /* positions labelled 1-10, not 0-9 */
        scores[playerindex] += positions[playerindex] + 1;
        DBGPRINT("--- dice roll %lu, player %d at position %u, score %lu\n",
                diceroll, playerindex, positions[playerindex],
                scores[playerindex]);
        if(scores[playerindex] >= WINNINGSCORE)
            done = 1;
    }


    /* print results for all players */
    for(playerindex=0; playerindex < NPLAYERS; playerindex++)
    {
        printf("Player %d at score %lu after %lu rolls: final score %lu\n",
                playerindex + 1, scores[playerindex], diceroll - 1,
                scores[playerindex] * (diceroll - 1));
    }

    return 0;
}
#endif
