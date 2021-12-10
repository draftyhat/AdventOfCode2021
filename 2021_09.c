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

/* value indicating grid square has been counted. Must be greater than 9. */
#define COUNTED 10


struct grid {
    int height;
    int width;
    int ** values;
};

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
    for(int y=0; y < g->height; y++)
    {
        for(int x = 0; x < g->width; x++)
        {
            printf("%x", g->values[y][x]);
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

int count_all_connected(struct grid * g, int x, int y)
{
    int retval = 0;
    int newx, newy, newvalue;

    //DBGPRINT("  counting connected (%d,%d)\n", x, y);
    /* assume this point has been counted already */
    if(grid_get_up(&newvalue, &newx, &newy, g, x, y))
    {
        if(newvalue < 9)
        {
            grid_set_value(g, newx, newy, COUNTED);
            retval += 1;
            retval += count_all_connected(g, newx, newy);
        }
    }
    if(grid_get_down(&newvalue, &newx, &newy, g, x, y))
    {
        if(newvalue < 9)
        {
            grid_set_value(g, newx, newy, COUNTED);
            retval += 1;
            retval += count_all_connected(g, newx, newy);
        }
    }
    if(grid_get_left(&newvalue, &newx, &newy, g, x, y))
    {
        if(newvalue < 9)
        {
            grid_set_value(g, newx, newy, COUNTED);
            retval += 1;
            retval += count_all_connected(g, newx, newy);
        }
    }
    if(grid_get_right(&newvalue, &newx, &newy, g, x, y))
    {
        if(newvalue < 9)
        {
            grid_set_value(g, newx, newy, COUNTED);
            retval += 1;
            retval += count_all_connected(g, newx, newy);
        }
    }

    return retval;
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

    printf("Sum of the risk levels of all the low points: %d\n", risk_sum);

    /* now part 2 */
    int basin_sizes[1000];
    int basin_idx = 0;
    for(x=0; x < g.width; x++)
    {
        for(y=0; y < g.height; y++)
        {
            /* is this point in a basin? */
            DBGPRINT("Checking for basin at (%d,%d)\n", x, y);
            if(grid_get_value(&g, x, y) < 9)
            {
                /* set this value as counted */
                grid_set_value(&g, x, y, COUNTED);
                basin_sizes[basin_idx] = 1;

                /* count all points connected to this one that have value < 9 */
                DBGPRINT("Found new basin at (%d,%d)\n", x, y);
                basin_sizes[basin_idx] += count_all_connected(&g, x, y);
                basin_idx++;
                print_grid(&g);
            }
        }
    }

    int max_size_basins[3];
    int max_idx, this_basin_size, save;
    memcpy(max_size_basins, basin_sizes, sizeof(max_size_basins));
    DBGPRINT("basin sizes: %d %d %d", basin_sizes[0], basin_sizes[1], basin_sizes[2]);
    for(int i=sizeof(max_size_basins)/sizeof(max_size_basins[0]); i < basin_idx; i++)
    {
        DBGPRINT(" %d", basin_sizes[i]);
        this_basin_size = basin_sizes[i];
        for(max_idx = 0;
                max_idx < sizeof(max_size_basins)/sizeof(max_size_basins[0]);
                max_idx++)
        {
            if(this_basin_size > max_size_basins[max_idx])
            {
                /* can't just do a simple replace; the one replaced may be
                 * larger than one of the other maxes. */
                save = this_basin_size;
                this_basin_size = max_size_basins[max_idx];
                max_size_basins[max_idx] = save;
            }
        }
        DBGPRINT(" (%d %d %d)", max_size_basins[0], max_size_basins[1],
                max_size_basins[2]);
    }
    DBGPRINT("\n");

    int max_product = 1;
    DBGPRINT("Max size basins: ");
    for(max_idx = 0; max_idx < sizeof(max_size_basins)/sizeof(max_size_basins[0]); max_idx++)
    {
        DBGPRINT("%d ", max_size_basins[max_idx]);
        max_product *= max_size_basins[max_idx];
    }
    DBGPRINT("\n");

    printf("Max size basins: %d\n", max_product);
    print_grid(&g);

    free_grid(&g);

    return 0;
}

