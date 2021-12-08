#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

int calculate_fuel_abs(int abs_distance)
{
    int fuel;
#ifndef PART2
#error beep
    fuel = abs_distance;
#else  /* part 2 */
    fuel = 0;

    for(int i=1; i <= abs_distance; i++)
    {
        fuel += i;
    }
    printf("  fuel for distance %d: %d\n", abs_distance, fuel);
#endif
    return fuel;
}
int calculate_fuel(int current_position, const int * positions, int npositions)
{
    int fuel = 0, i;

    for(i=0; i < npositions; i++)
    {
        printf(" move %d to %d\n", current_position, positions[i]);
        if(current_position > positions[i])
            fuel += calculate_fuel_abs(current_position - positions[i]);
        else
            fuel += calculate_fuel_abs(positions[i] - current_position);
    }

    return fuel;
}


#ifdef TEST
const int test(position, fuel)
{
    struct {
        int position;
        int fuel;
    } answers[] =  {
#ifndef PART2
        {1, 41},
        {2, 37},
        {3, 39},
        {10, 71}
#else  /* PART2 */
        {2, 206},
        {5, 168}
#endif
    };

    for(int i=0; i < sizeof(answers)/sizeof(answers[0]); i++)
    {
        if(position = answers[i].position)
        {
            if(fuel == answers[i].fuel)
                return 1;
            DBGPRINT("TEST FAILED! position %d costs %d fuel, expected %d\n",
                    position, fuel, answers[i].fuel);
            return 0;
        }
    }
}
#endif


int main(int argc, char ** argv)
{
    /* start with the easy thing. Read in all the numbers, find minimum and
     * maximum, check distance between each discrete point and all given
     * points, return minimum.
     * so if X is our point and a,b,c,d... our input, we want to minimize:
     *  abs(X-a)+abs(X-b)+abs(X-c)
     * ok, I found some math on stackoverflow about bivalent residuals. Will
     * look into that later.
     */
    int positions[4096];
    int npositions=0;
    int position_min, position_max;
    int best_position, current_position;
    int best_fuel, current_fuel;

    scanf("%d", &positions[0]);
    position_min = positions[0];
    position_max = positions[0];
    npositions = 1;
    while(1 == scanf(",%d", &positions[npositions]))
    {
        if(positions[npositions] < position_min)
            position_min = positions[npositions];
        if(positions[npositions] > position_max)
            position_max = positions[npositions];
        npositions++;
    }

    DBGPRINT("Read %d positions: %d, %d, %d...\n", npositions, positions[0],
            positions[1],positions[2]);

    /* calculate fuel for all positions between min and max */
    best_position = position_min;
    best_fuel = calculate_fuel(position_min,
            positions, npositions);
    for(current_position = position_min; current_position <= position_max;
            current_position++)
    {
        current_fuel = calculate_fuel(current_position,
                positions, npositions);
        if(current_fuel < best_fuel)
        {
            best_fuel = current_fuel;
            best_position = current_position;
        }
#ifdef TEST
        if(!test(current_position, current_fuel))
        {
            DBGPRINT("TEST FAILED!");
            exit(1);
        }
#endif
    }

    printf("Best position %d (fuel %d)\n", best_position, best_fuel);
}
