#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "include/grid.h"


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define AOC_DAY 10
#define AOC_YEAR 2021

int add_energy(struct grid * g, int x, int y)
{
    int value;

    DBGPRINT("adding energy (%d,%d)\n", x, y);

    /* returns 1 if octopus flashes right now; else 0 */
    value = grid_get_value(g, x, y) + 1;
    grid_set_value(g, x, y, value);
    if(10 == value)
    {
        /* this octopus just flashed! */
        return 1;
    }

    return 0;
}

void energize_adjacent(struct grid * g, int x, int y)
{
    int tmpx, tmpy;
    /* energizing all connected octopi (including diagonals) */
    DBGPRINT("ENERGIZE ADJACENT (%d,%d)\n", x, y);
    tmpx = x - 1;
    if(tmpx >= 0)
    {
        /* left column */
        for(tmpy = y - 1; tmpy <= y + 1; tmpy++)
        {
            if(tmpy >= 0 && tmpy < g->height)
            {
                if(add_energy(g, tmpx, tmpy))
                    /* this octopus just flashed! */
                    energize_adjacent(g, tmpx, tmpy);
            }
        }
    }
    /* top */
    if(y - 1 >= 0)
    {
        if(add_energy(g, x, y - 1))
            /* this octopus just flashed! */
            energize_adjacent(g, x, y - 1);
    }
    if(y + 1 < g->height)
    {
        if(add_energy(g, x, y + 1))
            /* this octopus just flashed! */
            energize_adjacent(g, x, y + 1);
    }
    /* bottom */
    tmpx = x + 1;
    if(tmpx < g->width)
    {
        /* right column */
        for(tmpy = y - 1; tmpy <= y + 1; tmpy++)
        {
            if(tmpy >= 0 && tmpy < g->height)
            {
                if(add_energy(g, tmpx, tmpy))
                    /* this octopus just flashed! */
                    energize_adjacent(g, tmpx, tmpy);
            }
        }
    }
    DBGPRINT("  DONE ENERGIZE ADJACENT (%d,%d)\n", x, y);
}

unsigned long energize_octopi(struct grid * g)
{
    unsigned long nflashes = 0;
    int x, y, value;

    /* add 1 energy to all octopi, and if flash, energize adjacent */
    for(x=0; x < g->width; x++)
    {
        for(y=0; y < g->height; y++)
        {
            value = grid_get_value(g, x, y) + 1;
            grid_set_value(g, x, y, value);
            if(10 == value)
            {
                energize_adjacent(g, x, y);
            }
        }
    }

    /* set every octopus that was a 10 back to 0 */
    for(x=0; x < g->width; x++)
    {
        for(y=0; y < g->height; y++)
        {
            if(grid_get_value(g, x, y) >= 10)
            {
                nflashes++;
                grid_set_value(g, x, y, 0);
            }
        }
    }

    return nflashes;
}

int main(int argc, char ** argv)
{
    struct grid g;
    unsigned long nflashes = 0, nflashes_this_step;
    int first_total_flash = -1;

    read_grid(&g, NULL);

    for(int step = 0; step < 100 || -1 == first_total_flash; step++)
    {
        nflashes_this_step = energize_octopi(&g);
        if(step < 100)
            nflashes += nflashes_this_step;
        printf("%d (need %d)\n", nflashes_this_step, g.width * g.height);
        if((-1 == first_total_flash) \
                && (nflashes_this_step == g.width * g.height))
        {
            first_total_flash = step;
        }
    }

    printf("After 100 steps: %lu flashes\n", nflashes);
    printf("First total flash: %d\n", first_total_flash + 1);

    free_grid(&g);
    return 0;
}

