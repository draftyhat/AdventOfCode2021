#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define AGEAFTERBIRTH 8
#define MAXAGE AGEAFTERBIRTH
#define AGEAFTERBREED 6

/* thanks to djotaku for telling me how to do this! */
unsigned long calculate_schoolsize(unsigned long school[MAXAGE + 1], unsigned long ndays)
{
    unsigned long save;
    unsigned long retval = 0;
    unsigned long i;

    /* school: fish at index n will breed in n days */

    for(i=0; i < ndays; i++)
    {
        save = school[0];
        /* move forward one day. All fish now have n-1 days to breed. */
        memmove(&school[0], &school[1], sizeof(school[0]) * MAXAGE);
        /* fish at 0 breed today */
        school[MAXAGE] = save;
        /* fish at 0 move to age AGEAFTERBREED */
        school[AGEAFTERBREED] += save;
    }

    /* count all the fish */
    retval = 0;
    for(i=0; i <= MAXAGE; i++)
    {
        retval += school[i];
    }

    return retval;
}
    

int main(int argc, char ** argv)
{
    unsigned long school[MAXAGE + 1];
    unsigned long scanf_retval;
    int age;

    /* initialize school by reading in fish ages */
    memset(school, 0, sizeof(school));
    scanf_retval = scanf("%d", &age);
    while(1 == scanf_retval)
    {
        /* add this fish to the school group that's this fish's age */
        school[age]++;
        scanf_retval = scanf(",%d", &age);
    }

    printf("school size after 18 days: %lu\n",
            calculate_schoolsize(school, 18));
    printf("school size after 80 days: %lu\n",
            calculate_schoolsize(school, 80-18));
    printf("school size after 256 days: %lu\n",
            calculate_schoolsize(school, 256-80));

    return 0;
}

