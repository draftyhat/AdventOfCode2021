#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "grid.h"


#ifdef DEBUG_GRID
#define DBGPRINT_GRID(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT_GRID(...)
#endif

#define AOC_DAY 9
#define AOC_YEAR 2021

/* value indicating grid square has been counted. Must be greater than 9. */
#define COUNTED 10


int grid_get_value(const struct grid * g, int x, int y)
{
    return g->values[y][x];
}

void grid_set_value(struct grid * g, int x, int y, int value)
{
    g->values[y][x] = value;
}

int grid_get_up(int * value, int * newx, int * newy,
        const struct grid * g, int x, int y)
{
    int retval = 1;
    *newx = x;
    *newy = y - 1;
    if(*newy < 0)
    {
        *newy = 0;
        retval = 0;
    }
    *value = g->values[*newy][*newx];

    return retval;
}

int grid_get_down(int * value, int * newx, int * newy,
        const struct grid * g, int x, int y)
{
    int retval = 1;
    *newx = x;
    *newy = y + 1;
    if(*newy >= g->height)
    {
        *newy = y;
        retval = 0;
    }
    *value = g->values[*newy][*newx];
    return retval;
}

int grid_get_right(int * value, int * newx, int * newy,
        const struct grid * g, int x, int y)
{
    int retval = 1;
    *newx = x + 1;
    *newy = y;
    if(*newx >= g->width)
    {
        *newx = x;
        retval = 0;
    }
    *value = g->values[*newy][*newx];
    return retval;
}

int grid_get_left(int * value, int * newx, int * newy,
        const struct grid * g, int x, int y)
{
    int retval = 1;
    *newx = x - 1;
    *newy = y;
    if(*newx < 0)
    {
        *newx = x;
        retval = 0;
    }
    *value = g->values[*newy][*newx];
    return retval;
}

int read_grid(struct grid * g)
{
    char line[4096];
    int * rows[1000];
    int rown = 0;
    int scanf_retval;
    int i;

    /* read the first line, figure out how wide our grid is */
    scanf_retval = scanf("%s", line);
    g->width = strlen(line);
    DBGPRINT_GRID("DBG grid: width %d\n", g->width);

    while(1 == scanf_retval)
    {
        /* allocate new row */
        rows[rown] = (int *) malloc(sizeof(g->values[0][0]) * g->width);
        DBGPRINT_GRID("DBG grid: reading row %d: ", rown);
        /* convert characters into ints for row array */
        for(i=0; i < g->width; i++)
        {
            rows[rown][i] = line[i] - '0';
            DBGPRINT_GRID("%d", rows[rown][i]);
        }
        DBGPRINT_GRID("\n");

        /* read next line */
        scanf_retval = scanf("%s", line);
        rown++;
    }

    DBGPRINT_GRID("DBG grid: read %d rows\n", rown);

    /* allocate values array for grid, copy pointers into that */
    g->height = rown;
    g->values = (int **) malloc(sizeof(g->values[0]) * rown);
    memcpy(g->values, rows, sizeof(rows[0]) * g->height);

    return 0;
}

void free_grid(struct grid * g)
{
    for(int rown = 0; rown < g->height; rown++)
        free(g->values[rown]);
    free(g->values);
    g->values = NULL;
}

void print_grid(const struct grid * g)
{
    for(int y=0; y < g->height; y++)
    {
        for(int x = 0; x < g->width; x++)
        {
            printf("%x", g->values[y][x]);
        }
        printf("\n");
    }
}


#ifdef TEST_GRID
int main(int argc, char ** argv)
{
    /* write some test code... */
}
#endif
