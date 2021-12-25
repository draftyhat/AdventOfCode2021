#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifdef TEST
/* target area: x=20..30, y=-10..-5 */
#define TARGET_X0 20
#define TARGET_X1 30
#define TARGET_Y0 -10
#define TARGET_Y1 -5
#else
/* target area: x=25..67, y=-260..-200 */
#define TARGET_X0 25
#define TARGET_X1 67
#define TARGET_Y0 -260
#define TARGET_Y1 -200
#endif


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define AOC_DAY 9
#define AOC_YEAR 2021

int get_next_position(int * xposition, int * yposition,
        int * xvelocity, int * yvelocity)
{
    *xposition += *xvelocity;
    *yposition += *yvelocity;

    if(*xvelocity > 0)
        (*xvelocity)--;
    else if(*xvelocity < 0)
        (*xvelocity)++;
    (*yvelocity)--;

    DBGPRINT("(%d,%d) traveling [%d,%d]\n", *xposition, *yposition,
            *xvelocity, *yvelocity);

    return 0;
}

/* returns 1 if in bounds, -1 if will never be in bounds, 0 if not in bounds
 * but might be on a future step */
int check_in_bounds(int xposition, int yposition, int xvelocity)
{
    if(xposition > TARGET_X1)
        return -1;
    if(yposition < TARGET_Y0)
        return -1;

    if(TARGET_X0 <= xposition && xposition <= TARGET_X1)
    {
        if(TARGET_Y0 <= yposition && yposition <= TARGET_Y1)
        {
            return 1;
        }
    }
    else
    {
        if(0 == xvelocity)
            /* not in x range, and x position will never change */
            return -1;
    }
    return 0;
}

int main(int argc, char ** argv)
{
    int xvelocity, yvelocity, initial_xvelocity, initial_yvelocity;
    int xposition, yposition;
    int max_height = 0, this_height = 0;
    int bounds_determination;
    int nsuccesses = 0;

    for(initial_xvelocity = 1; initial_xvelocity <= TARGET_X1;
            initial_xvelocity++)
    {
        for(initial_yvelocity = TARGET_Y0; initial_yvelocity < 1000; initial_yvelocity++)
        {
            xposition = 0;
            yposition = 0;
            this_height = 0;
            xvelocity = initial_xvelocity;
            yvelocity = initial_yvelocity;
            get_next_position(&xposition, &yposition,
                    &xvelocity, &yvelocity);
            bounds_determination = check_in_bounds(xposition,
                    yposition, xvelocity);
            if(yposition > this_height)
                this_height = yposition;
            while(0 == bounds_determination)
            {
                get_next_position(&xposition, &yposition,
                        &xvelocity, &yvelocity);
                bounds_determination = check_in_bounds(xposition,
                        yposition, xvelocity);
                if(yposition > this_height)
                    this_height = yposition;
            }
            if(1 == bounds_determination)
            {
                nsuccesses++;
printf("success %d,%d\n", initial_xvelocity, initial_yvelocity);
                if(this_height > max_height)
                {
                    DBGPRINT("Found new max_height %d with velocities (%d,%d)\n",
                            this_height, initial_xvelocity, initial_yvelocity);
                    max_height = this_height;
                }
            }
        }
    }

    printf("max height %d\n", max_height);
    printf("nsuccesses %d\n", nsuccesses);

    return 0;
}

