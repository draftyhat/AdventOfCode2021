#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define NDAYS 80
#define NDAYSAFTERBIRTH 9
#define NDAYSAFTERBREED 7
#define ENDOFTIME (NDAYS + NDAYSAFTERBIRTH)
#define STARTOFTIME (NDAYSAFTERBIRTH)

/* the number of fish in the school, if the first fish was born on day n */
static int schoolsize[ENDOFTIME];

void calculate_schoolsize()
{
    int nfish_born[ENDOFTIME];
    int nfish_born_today, schoolsize_today;

    /* calculate from the back */
    /* fish born within the last 9 days of the end of time have no offspring
     * */
    for(int i=0; i < NDAYSAFTERBIRTH; i++)
    {
        schoolsize[ENDOFTIME - i] = 1;
        nfish_born[ENDOFTIME - i] = 0;
    }

    /* A fish born at day ENDOFTIME - NDAYSAFTERBIRTH will have one offspring.
     * It will give birth to a new offspring 7 days after that. Furthermore,
     * each of those offspring will produce fish in the same pattern as their
     * parent fish, offset by 9 days.

                 11111111112222222222333333333344444444445555555555
       012345678901234567890123456789012345678901234567890123456789
mom    .........*......*......*......*......*......*......*......*.
child1          .........*......*......*......*......*......*......
child2                 .........*......*......*......*......*......
gchild11                 .........*......*......*......*......*....
child3                        .........*......*......*......*......
gchild12                        .........*......*......*......*....
gchild21                        .........*......*......*......*....
ggchild111                        .........*......*......*......*..
...

     */


    schoolsize[ENDOFTIME - 1] = 1;
    nfish_born[ENDOFTIME - 1] = 0;
    for(int i = ENDOFTIME - 2; i >= 0; i--)
    {
        nfish_born_today = 0;
        schoolsize_today = schoolsize[i+1];
        /* on day i:
         *  1 fish is born if it's Mom's day to give birth, so if 
         *      (i + NDAYSAFTERBIRTH) < ENDOFTIME
         *      and (i + NDAYSAFTERBIRTH) % 7 == 0
         *  plus the count of all fish birthed by Mom's offspring. So,
         *      (i + NDAYSAFTERBIRTH) + 7x, for all x such that that number <
         *      ENDOFTIME.
         */

        /* if Mom is old enough to have offspring */
        if(i + NDAYSAFTERBIRTH < ENDOFTIME)
        {
            /* is it Mom's turn to give birth? */
            if((i - NDAYSAFTERBIRTH) % NDAYSAFTERBREED == 0)
                nfish_born_today++;
            for(int x = i + NDAYSAFTERBIRTH;
                    x < ENDOFTIME;
                    x += NDAYSAFTERBREED)
            {
                nfish_born_today += nfish_born[x];
            }
        }

        nfish_born[i] = nfish_born_today;
        schoolsize[i] = schoolsize_today + nfish_born_today;
    }
}



int main(int argc, char ** argv)
{
    int age;
    int scanf_retval;
    int nfish_18days = 0;
    int nfish_80days = 0;

    calculate_schoolsize();

    scanf_retval = scanf("%d", &age);
    while(1 == scanf_retval)
    {
        DBGPRINT("Processing age %d\n", age);
        /* Mom was born on day NDAYSAFTERBIRTH - age, so reaches 80
         * at 80 + (NDAYSAFTERBIRTH - age) */
        nfish_18days += schoolsize[80 - 18 + (NDAYSAFTERBIRTH - age)];
        nfish_80days += schoolsize[NDAYSAFTERBIRTH - age];
        scanf_retval = scanf(",%d", &age);
    }
    for(int q=0; q < sizeof(schoolsize)/sizeof(schoolsize[0]); q++)
    {
        if(q % 8 == 0)
            DBGPRINT("\n%2d:", q);
        DBGPRINT(" %4d", schoolsize[q]);
    }
    DBGPRINT("\n");

    printf("After 18 days, there are %d fish\n", nfish_18days);
    printf("After 80 days, there are %d fish\n", nfish_80days);
}
