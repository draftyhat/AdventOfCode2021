#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif

#define MESSAGE_LENGTH 12

/* very similar to 2016 day 6 */

int main(int argc, char ** argv)
{
    char message[MESSAGE_LENGTH + 1];
    int freqs[MESSAGE_LENGTH][2];
    int i;
    int gamma = 0, epsilon = 0;

    memset(freqs, 0, sizeof(freqs));

    /* read in each message and log its characters */
    while(1 == scanf("%s", message))
    {
        for(i=0; i < MESSAGE_LENGTH; i++)
        {
            if('0' == message[i])
                freqs[i][0]++;
            else if('1' == message[i])
                freqs[i][1]++;
        }
    }

    /* for each column, pick out the target character */
    for(i=0; i < MESSAGE_LENGTH; i++)
    {
        /* if 0 is the most common, shift both gamma and epsilon left 1 and add
         * 1 to epsilon */
        if(freqs[i][0] > freqs[i][1])
        {
            gamma = gamma << 1;
            epsilon = (epsilon << 1) + 1;
        }
        /* else if 1 is most common, shift both and add one to gamma */
        else
        {
            gamma = (gamma << 1) + 1;
            epsilon = epsilon << 1;
        }
    }
    DBGPRINT("gamma: %d (%x)\n", gamma, gamma);
    DBGPRINT("epsilon: %d (%x)\n", epsilon, epsilon);

    printf("%d\n", gamma * epsilon);
}
