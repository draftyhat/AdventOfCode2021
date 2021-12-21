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


#define NITERATIONS 50

void enhance_image(struct grid * image, int iea[512])
{
    int x, y, xiter, yiter;
    int iea_index;
    struct grid newimage;

    /* initialize a new grid */
    create_grid(&newimage, image->width, image->height, 0);

    for(x=2; x < image->width; x++)
    {
        for(y=2; y < image->height; y++)
        {
            /* create the 9-bit number indicated by the 3x3 square starting at
             * x-2, y-2 */
            iea_index = 0;
            for(yiter = y-2; yiter <= y; yiter++)
            {
                for(xiter = x-2; xiter <= x; xiter++)
                {
                    iea_index = (iea_index << 1)
                        | grid_get_value(image, xiter, yiter);
                }
            }

            /* pull the indicated value from the iea, and put it in the new
             * image */
            grid_set_value(&newimage, x-1, y-1, iea[iea_index]);
        }
    }

    /* replace the old grid */
    free_grid(image);
    memcpy(image, &newimage, sizeof(newimage));
}

int main(int argc, char ** argv)
{
    int translation[256];
    int iea[512];
    int i;
    char ch;
    struct grid image;
    int iteration;

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

    /* extend image so there's room for enhancement */
    extend_grid(&image,
            image.width + NITERATIONS * 4, image.height + NITERATIONS * 4,
            NITERATIONS * 2, NITERATIONS * 2, 0);

    /* enhance */
    for(iteration = 0; iteration < NITERATIONS; iteration++)
    {
        enhance_image(&image, iea);
    }
    print_grid(&image);

    /* count number of lit pixels */
    printf("Found %lu lit pixels\n", sum_subgrid(&image,
                NITERATIONS, NITERATIONS, image.width - NITERATIONS, image.height - NITERATIONS));
}
