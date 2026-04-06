#include <stdbool.h>

int result = 0;

int add(int x, int y) {
    return (x + y);
}

int subtract(int x, int y) {
    return (x - y);
}

int multiply(int x, int y) {
    return (x * y);
}

int divide(int x, int y) {
    if ((y == 0)) {
        return 0;
    }
    return (x / y);
}

int max(int x, int y) {
    if ((x > y)) {
        return x;
    }
    return y;
}

int min(int x, int y) {
    if ((x < y)) {
        return x;
    }
    return y;
}

void main(void) {
    int a = 20;
    int b = 5;
    (result = add(a, b));
    (result = subtract(result, 3));
    (result = multiply(result, 2));
    (result = divide(result, b));
    (result = max(result, 10));
    (result = min(result, 50));
}
