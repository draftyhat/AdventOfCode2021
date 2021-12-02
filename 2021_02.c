#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#ifdef PART2
#define WINDOW_SIZE 3
#else
#define WINDOW_SIZE 1
#endif

#define MAX_VECTOR 1000


int main(int argc, char ** argv)
{
    char vector[MAX_VECTOR];
    int magnitude;
    int x=0,y=0, aim=0;

    /* read direction and magnitude from stdin */
    while(2 == scanf("%s %d", vector, &magnitude))
    {
        /* translate string vector to coordinates, multiply by magnitude, and
         * add to current position */
#ifdef PART2
        if(0 == strcmp("forward", vector))
        {
            x += magnitude; 
            y += aim * magnitude;
        }
        else if(0 == strcmp("up", vector))
        {
            aim -= magnitude;
        }
        else if(0 == strcmp("down", vector))
        {
            aim += magnitude;
        }
#else /* part 1 */
        /* translate string vector to coordinates, multiply by magnitude, and
         * add to current position */
        if(0 == strcmp("forward", vector))
            x += magnitude; 
        else if(0 == strcmp("up", vector))
            y -= magnitude;
        else if(0 == strcmp("down", vector))
            y += magnitude;
#endif
    }
    DBGPRINT("Final position: (%d, %d)\n", x, y);

    printf("%d\n", x * y);
}
