#include <stdbool.h>

void delay(int ms);
void screen_clear(void);
void screen_print(int x, int y, const char *text);
void screen_update(void);

int hunger = 0;
int happiness = 100;
int health = 100;
bool sick = false;

void feed(void) {
    (hunger = 0);
}

void tick(void) {
    (hunger = (hunger + 1));
    if ((hunger > 10)) {
        (health = (health - 1));
    }
}

void draw(void) {
    screen_clear();
    screen_print(0, 0, "PET");
    screen_print(0, 10, "HUNGER");
    screen_update();
}

void main_loop(void) {
    while (true) {
        tick();
        draw();
        delay(1000);
    }
}
