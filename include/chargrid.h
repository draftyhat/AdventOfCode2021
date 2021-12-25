#ifndef CHARGRID_H
#define CHARGRID_H

/*
 * A simple chargrid implementation
 * #define DEBUG_CHARGRID for debugging
 * Compile with TEST_CHARGRID for unit tests
 */


struct chargrid {
    int height;
    int width;
    char ** values;
};

char chargrid_get_value(const struct chargrid * g, int x, int y);

void chargrid_set_value(struct chargrid * g, int x, int y, char value);

int chargrid_get_up(char * value, int * newx, int * newy,
        const struct chargrid * g, int x, int y);

int chargrid_get_down(char * value, int * newx, int * newy,
        const struct chargrid * g, int x, int y);

int chargrid_get_right(char * value, int * newx, int * newy,
        const struct chargrid * g, int x, int y);

int chargrid_get_left(char * value, int * newx, int * newy,
        const struct chargrid * g, int x, int y);

void create_chargrid(struct chargrid * g, int width, int height, char
        default_value);

int read_chargrid(struct chargrid * g, char * translation);
/* allocate more chargrid space. move current chargrid to x0, y0, and extend
 * dimensions */
int extend_chargrid(struct chargrid * g, int new_width, int new_height, int x0,
        int y0, char default_value);

void free_chargrid(struct chargrid * g);


void print_chargrid(const struct chargrid * g);
void print_chargrid_section(const struct chargrid * g, int x0, int x1, int y0, int y1);




#endif  /* #ifndef CHARGRID_H */

