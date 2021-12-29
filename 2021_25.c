#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "include/chargrid.h"


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define AOC_DAY 25
#define AOC_YEAR 2021

int move_east(struct chargrid * g)
{
    int x, y;
    char save;
    int moved = 0;

    for(y = 0; y < g->height; y++)
    {
        save = chargrid_get_value(g, 0, y);
        for(x = 1; x < g->width; x++)
        {
            if('>' == chargrid_get_value(g, x - 1, y)
                    && '.' == chargrid_get_value(g, x, y))
            {
                /* move this guy one right */
                chargrid_set_value(g, x-1, y, '.');
                chargrid_set_value(g, x, y, '>');
                moved++;
                /* skip next calculation; we know that spot was a '.' */
                x++;
            }
        }
        /* check wraparound spot. We saved g(0, y) in save. */
        if(x == g->width
                && '>' == chargrid_get_value(g, g->width - 1, y)
                && '.' == save)
        {
            chargrid_set_value(g, g->width - 1, y, '.');
            chargrid_set_value(g, 0, y, '>');
            moved++;
        }
    }
    return moved;
}
int move_south(struct chargrid * g)
{
    int x, y;
    char save;
    int moved = 0;

    for(x = 0; x < g->width; x++)
    {
        save = chargrid_get_value(g, x, 0);
        for(y = 1; y < g->height; y++)
        {
            if('v' == chargrid_get_value(g, x, y - 1)
                    && '.' == chargrid_get_value(g, x, y))
            {
                /* move this guy one down */
                chargrid_set_value(g, x, y-1, '.');
                chargrid_set_value(g, x, y, 'v');
                moved++;
                /* skip next calculation; we know that spot was a '.' */
                y++;
            }
        }
        /* check wraparound spot. We saved g(0, y) in save. */
        if(y == g->height
                && 'v' == chargrid_get_value(g, x, g->height - 1)
                && '.' == save)
        {
            chargrid_set_value(g, x, g->height - 1, '.');
            chargrid_set_value(g, x, 0, 'v');
            moved++;
        }
    }
    return moved;
}

int main(int argc, char ** argv)
{
    struct chargrid g;
    int moved = 1;
    int nrounds;

    read_chargrid(&g, NULL);
#ifdef TEST
    print_chargrid(&g);
    printf("-- moving east\n");
    moved = move_east(&g);
    print_chargrid(&g);
    printf(" -- moving south\n");
    moved += move_south(&g);
    print_chargrid(&g);
#else

    for(nrounds = 0; moved > 0; nrounds++)
    {
        moved = move_east(&g);
        moved += move_south(&g);
        printf("-- ROUND %d\n", nrounds);
        print_chargrid(&g);
    }
#endif

    printf("%d rounds\n", nrounds);

    return 0;
}

