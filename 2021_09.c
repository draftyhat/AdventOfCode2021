#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define AOC_DAY 9
#define AOC_YEAR 2021


struct grid {
    int height;
    int width;
    int ** values;
};

int grid_get_value(const struct grid * g, int x, int y)
{
    return g->values[y][x];
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
    DBGPRINT("DBG grid: width %d\n", g->width);

    while(1 == scanf_retval)
    {
        /* allocate new row */
        rows[rown] = (int *) malloc(sizeof(g->values[0][0]) * g->width);
        DBGPRINT("DBG grid: reading row %d: ", rown);
        /* convert characters into ints for row array */
        for(i=0; i < g->width; i++)
        {
            rows[rown][i] = line[i] - '0';
            DBGPRINT("%d", rows[rown][i]);
        }
        DBGPRINT("\n");

        /* read next line */
        scanf_retval = scanf("%s", line);
        rown++;
    }

    DBGPRINT("DBG grid: read %d rows\n", rown);

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
    for(int x = 0; x < g->width; x++)
    {
        for(int y=0; y < g->height; y++)
        {
            printf("%d", g->values[y][x]);
        }
        printf("\n");
    }
}

int is_low_point(const struct grid * g, int x, int y)
{
    int newx, newy, newvalue;
    int thisvalue = grid_get_value(g, x, y);

    DBGPRINT("Checking point (%d,%d), value %d\n", x, y, thisvalue);

    /* check all directions */
    if(grid_get_up(&newvalue, &newx, &newy, g, x, y))
    {
        if(newvalue <= thisvalue)
        {
            DBGPRINT(" point to up, (%d,%d), has lesser value %d\n",
                    newx, newy, newvalue);
            return 0;
        }
    }
    if(grid_get_down(&newvalue, &newx, &newy, g, x, y))
    {
        if(newvalue <= thisvalue)
        {
            DBGPRINT(" point to down, (%d,%d), has lesser value %d\n",
                    newx, newy, newvalue);
            return 0;
        }
    }
    if(grid_get_left(&newvalue, &newx, &newy, g, x, y))
    {
        if(newvalue <= thisvalue)
        {
            DBGPRINT(" point to left, (%d,%d), has lesser value %d\n",
                    newx, newy, newvalue);
            return 0;
        }
    }
    if(grid_get_right(&newvalue, &newx, &newy, g, x, y))
    {
        if(newvalue <= thisvalue)
        {
            DBGPRINT(" point to right, (%d,%d), has lesser value %d\n",
                    newx, newy, newvalue);
            return 0;
        }
    }

    DBGPRINT("  found low point (%d,%d), value %d\n", x, y, thisvalue);
    return 1;
}

int main(int argc, char ** argv)
{
    struct grid g;
    int x, y;
    int risk_sum = 0;

    read_grid(&g);

    for(x=0; x < g.width; x++)
    {
        for(y=0; y < g.height; y++)
        {
            if(is_low_point(&g, x, y))
            {
                risk_sum += grid_get_value(&g, x, y) + 1;
            }
        }
    }

    free_grid(&g);

    printf("Sum of the risk levels of all the low points: %d\n", risk_sum);


    return 0;
}

