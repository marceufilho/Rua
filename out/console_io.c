#include <stdbool.h>

void rua_print_string(const char *value);
void rua_println_string(const char *value);
const char *rua_read_line(void);

void main(void) {
    rua_print_string("Qual e o seu nome? ");
    const char *name = rua_read_line();
    rua_print_string("Ola, ");
    rua_println_string(name);
}
