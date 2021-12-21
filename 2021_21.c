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
#define WINNINGSCORE 1000
#define NPOSITIONS 10

int main(int argc, char ** argv)
{
    int positions[NPLAYERS];
    unsigned long scores[NPLAYERS];
    int playerindex;
    unsigned long diceroll;
    int done;
    int turnroll;


    memset(scores, 0, sizeof(scores));
           
#ifdef TEST
    positions[0] = 4 - 1;
    positions[1] = 8 - 1;
#else
    positions[0] = 1 - 1;
    positions[1] = 3 - 1;
#endif

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
