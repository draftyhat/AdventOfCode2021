#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <grid.h>


#ifdef DEBUG
#define DBGPRINT(...) fprintf(stderr, __VA_ARGS__)
#else
#define DBGPRINT(...)
#endif


#define NITERATIONS 2


int main(int argc, char ** argv)
{
    int translation[256];
    int iea[512];
    int i;
    char ch;
    struct grid image;

    /* create translation matrix */
    memset(translation, 0, sizeof(translation));
    translation[(int) '#'] = 1;

    /* read iea */
    scanf("%c", &ch);
    for(i=0; i < sizeof(iea)/sizeof(iea[0]); i++)
    {
        iea[i] = translation[(int) ch];
        scanf("%c", &ch);
    }

    printf("ended at %02x\n", ch);
    if('\n' != ch)
    {
        printf("ERROR: expected 512-byte iea\n");
        return 1;
    }

    /* read image */
    scanf("\n");
    read_grid(&image, translation);
    printf("read image:\n");
    print_grid(&image);

    /* extend image so there's room for enhancement */
    extend_grid(&image, image.width + NITERATIONS * 2, image.height + NITERATIONS * 2,
           NITERATIONS, NITERATIONS, 0);

    printf("image:\n");
    print_grid(&image);
}
