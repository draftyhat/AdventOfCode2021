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

void create_grid(struct grid * g, int width, int height, int default_value);

int read_grid(struct grid * g, int * translation);
/* allocate more grid space. move current grid to x0, y0, and extend dimensions
 * */
int extend_grid(struct grid * g, int new_width, int new_height, int x0, int y0,
        int default_value);

void free_grid(struct grid * g);

void print_grid(const struct grid * g);
void print_grid_section(const struct grid * g, int x0, int x1, int y0, int y1);


unsigned long sum_grid(struct grid * g);
unsigned long sum_subgrid(struct grid * g, int x, int y, int width, int height);


#endif  /* #ifndef GRID_H */

