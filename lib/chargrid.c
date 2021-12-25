#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "chargrid.h"


#ifdef DEBUG_CHARGRID
#define DBGPRINT_CHARGRID(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT_CHARGRID(...)
#endif

#define AOC_DAY 9
#define AOC_YEAR 2021

/* value indicating chargrid square has been counted. Must be greater than 9. */
#define COUNTED 10


char chargrid_get_value(const struct chargrid * g, int x, int y)
{
    return g->values[y][x];
}

void chargrid_set_value(struct chargrid * g, int x, int y, char value)
{
    g->values[y][x] = value;
}

int chargrid_get_up(char * value, int * newx, int * newy,
        const struct chargrid * g, int x, int y)
{
    int retval = 1;
    *newx = x;
    *newy = y - 1;
    if(*newy < 0)
    {
        *newy = g->height - 1;
        retval = 0;
    }
    *value = g->values[*newy][*newx];

    return retval;
}

int chargrid_get_down(char * value, int * newx, int * newy,
        const struct chargrid * g, int x, int y)
{
    int retval = 1;
    *newx = x;
    *newy = y + 1;
    if(*newy >= g->height)
    {
        *newy = 0;
        retval = 0;
    }
    *value = g->values[*newy][*newx];
    return retval;
}

int chargrid_get_right(char * value, int * newx, int * newy,
        const struct chargrid * g, int x, int y)
{
    int retval = 1;
    *newx = x + 1;
    *newy = y;
    if(*newx >= g->width)
    {
        *newx = 0;
        retval = 0;
    }
    *value = g->values[*newy][*newx];
    return retval;
}

int chargrid_get_left(char * value, int * newx, int * newy,
        const struct chargrid * g, int x, int y)
{
    int retval = 1;
    *newx = x - 1;
    *newy = y;
    if(*newx < 0)
    {
        *newx = g->width - 1;
        retval = 0;
    }
    *value = g->values[*newy][*newx];
    return retval;
}

void create_chargrid(struct chargrid * g, int width, int height,
        char default_value)
{
    g->width = width;
    g->height = height;
    g->values = (char **) malloc(sizeof(g->values[0]) * height);
    for(int rown=0; rown < height; rown++)
    {
        g->values[rown] = (char *) malloc(sizeof(g->values[0][0]) * width);
        for(int coln = 0; coln < width; coln++)
            g->values[rown][coln] = default_value;
    }
}

int read_chargrid(struct chargrid * g, char * translation)
{
    char line[4096];
    char * rows[1000];
    int rown = 0;
    int scanf_retval;
    int i;

    /* read the first line, figure out how wide our chargrid is */
    scanf_retval = scanf("%s", line);
    g->width = strlen(line);
    DBGPRINT_CHARGRID("DBG chargrid: width %d\n", g->width);

    while(1 == scanf_retval)
    {
        /* allocate new row */
        rows[rown] = (char *) malloc(sizeof(g->values[0][0]) * g->width);
        DBGPRINT_CHARGRID("DBG chargrid: reading row %d: ", rown);
        /* convert characters into ints for row array */
        if(translation)
        {
            for(i=0; i < g->width; i++)
            {
                rows[rown][i] = translation[ (int) line[i]];
                DBGPRINT_CHARGRID("%c", rows[rown][i]);
            }
        }
        else
        {
            for(i=0; i < g->width; i++)
            {
                rows[rown][i] = line[i];
                DBGPRINT_CHARGRID("%c", rows[rown][i]);
            }
        }
        DBGPRINT_CHARGRID("\n");

        /* read next line */
        scanf_retval = scanf("%s", line);
        rown++;
    }

    DBGPRINT_CHARGRID("DBG chargrid: read %d rows\n", rown);

    /* allocate values array for chargrid, copy pointers into that */
    g->height = rown;
    g->values = (char **) malloc(sizeof(g->values[0]) * rown);
    memcpy(g->values, rows, sizeof(rows[0]) * g->height);

    return 0;
}

int extend_chargrid(struct chargrid * g, int new_width, int new_height, int x0,
        int y0, char default_value)
{
    int y, copy_width, copy_height;
    struct chargrid new_chargrid;

    /* allocate new chargrid */
    create_chargrid(&new_chargrid, new_width, new_height, default_value);

    /* copy data into new chargrid */
    copy_width = new_width - x0;
    if(copy_width > g->width)
        copy_width = g->width;
    copy_height = new_height - y0;
    if(copy_height > g->height)
        copy_height = g->height;
    for(y=0; y < copy_height; y++)
    {
        memcpy(&new_chargrid.values[y0 + y][x0], g->values[y],
                copy_width * sizeof(new_chargrid.values[0][0]));
    }

    /* free old chargrid */
    free_chargrid(g);

    /* set new values */
    g->values = new_chargrid.values;
    g->width = new_chargrid.width;
    g->height = new_chargrid.height;

    return 0;
}

void free_chargrid(struct chargrid * g)
{
    for(int rown = 0; rown < g->height; rown++)
        free(g->values[rown]);
    free(g->values);
    g->values = NULL;
}

void print_chargrid(const struct chargrid * g)
{
    for(int y=0; y < g->height; y++)
    {
        for(int x = 0; x < g->width; x++)
        {
            printf("%c", g->values[y][x]);
        }
        printf("\n");
    }
}

void print_chargrid_section(const struct chargrid * g, int x0, int x1, int y0, int y1)
{
    for(int y = y0; y < y1; y++)
    {
        for(int x = x0; x < x1; x++)
        {
            printf("%c", g->values[y][x]);
        }
        printf("\n");
    }
}


#ifdef TEST_CHARGRID
int main(int argc, char ** argv)
{
    /* write some test code... */
}
#endif

