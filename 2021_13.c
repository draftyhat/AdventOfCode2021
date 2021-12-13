#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "grid.h"


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define AOC_DAY 13
#define AOC_YEAR 2021


#ifndef TEST
#define GRID_WIDTH 1400
#define GRID_HEIGHT 1400
#else  /* TEST */
#define GRID_WIDTH 11
#define GRID_HEIGHT 15
#endif

void read_points(struct grid * g)
{
    int scanf_retval;
    int x, y;

    scanf_retval = scanf("%d,%d", &x, &y);
    while(2 == scanf_retval)
    {
        if(x >= g->width || y >= g->height)
        {
            printf("ERROR: found point (%d, %d) off grid of size (%d, %d)\n",
                    x, y, g->width, g->height);
            exit(1);
        }
        /* mark this point on the grid */
        grid_set_value(g, x, y, 1);
        scanf_retval = scanf("%d,%d", &x, &y);
    }
}

int read_folds(struct grid * g, unsigned int max_folds)
{
    char axis;
    int line;
    int scanf_retval;
    int foldn;
    int x, y;

    for(foldn=0; foldn < max_folds; foldn++)
    {
        scanf_retval = scanf("fold along %c=%d\n", &axis, &line);
        if(2 != scanf_retval)
        {
            foldn--;
            break;
        }
        if('x' == axis)
        {
            /* for each row */
            for(y=0; y < g->height; y++)
            {
                /* for each point on this row after the fold line */
                for(x = 0; x < g->width - line ; x++)
                {
                    if(1 == grid_get_value(g, line + x, y))
                    {
                        /* if this is a point, fold it */
                        grid_set_value(g, line - x, y, 1);
                        grid_set_value(g, line + x, y, 0);
                    }
                }
            }
        }
        else if('y' == axis)
        {
            /* for each column */
            for(x=0; x < g->height; x++)
            {
                /* for each point on this column below the fold line */
                for(y = 0; y < g->width - line ; y++)
                {
                    if(1 == grid_get_value(g, x, line + y))
                    {
                        /* if this is a point, fold it */
                        grid_set_value(g, x, line - y, 1);
                        grid_set_value(g, x, line + y, 0);
                    }
                }
            }
        }
    }
    return foldn;
}

int main(int argc, char ** argv)
{
    struct grid g;

    create_grid(&g, GRID_WIDTH, GRID_HEIGHT, 0);
#ifdef DEBUG
    print_grid(&g);
#endif

    /* fill in initial points */
    read_points(&g);
#ifdef DEBUG
    print_grid(&g);
#endif

    /* read fold marks */
    read_folds(&g, 1);
    /* count the number of dots */
    printf("After first fold, found %lu dots\n", sum_grid(&g));

    printf("made %u folds\n", read_folds(&g, (unsigned int) -1));
    print_grid_section(&g, 0, 40, 0, 6);

    for(int y = 0; y < 6; y++)
    {
        for(int x = 0; x < 40; x++)
        {
            if(1 == grid_get_value(&g, x, y))
                printf("#");
            else
                printf(" ");
        }
        printf("\n");
    }

    free_grid(&g);

    return 0;
}

