#ifndef GRID_H
#define GRID_H

/*
 * A simple grid implementation
 * #define DEBUG_GRID for debugging
 * Compile with TEST_GRID for unit tests
 */


struct grid {
    int height;
    int width;
    int ** values;
};

int grid_get_value(const struct grid * g, int x, int y);

void grid_set_value(struct grid * g, int x, int y, int value);

int grid_get_up(int * value, int * newx, int * newy,
        const struct grid * g, int x, int y);

int grid_get_down(int * value, int * newx, int * newy,
        const struct grid * g, int x, int y);

int grid_get_right(int * value, int * newx, int * newy,
        const struct grid * g, int x, int y);

int grid_get_left(int * value, int * newx, int * newy,
        const struct grid * g, int x, int y);

int read_grid(struct grid * g);

void free_grid(struct grid * g);

void print_grid(const struct grid * g);


#endif  /* #ifndef GRID_H */

