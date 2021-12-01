/* compile for keypad part 1: gcc -Wall -o 2021_02 2021_02.c */
/* compile for keypad part 2: gcc -DPART2 -Wall -o 2021_02 2021_02.c */
/* with debugging: gcc -DDEBUG -DPART2 -Wall -o 2021_02 2021_02.c */
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


int main(int argc, char ** argv)
{
    int last_depths[WINDOW_SIZE];
    int depth, increases = 0;
    int n = 0;

    /* stdin gets one depth measurement per line */
    /* fill in the window */
    while(n < WINDOW_SIZE && 1 == scanf("%d", &last_depths[n]))
        n++;

    /* add a depth measurement, check window for increase */
    while(1 == scanf("%d", &depth))
    {
        /* a + b + c < b + c + d
         * iff  a < d */
        if(depth > last_depths[n % WINDOW_SIZE])
            increases++;

        last_depths[n % WINDOW_SIZE] = depth;
        n++;
    }

    printf("%d\n", increases);
}
