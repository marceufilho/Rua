from pathlib import Path

from rua.c_transpiler import CTranspiler, transpile_to_c, write_c
from rua.parser import Parser
from rua.scanner import Scanner


def parse_source(source: str):
    return Parser(Scanner(source).scan_tokens()).parse()


def test_transpiles_single_global_declaration() -> None:
    program = parse_source("global hunger = 0;")

    expected = "\n".join(
        [
            "#include <stdbool.h>",
            "",
            "int hunger = 0;",
            "",
        ]
    )

    assert transpile_to_c(program) == expected


def test_transpiles_simple_function() -> None:
    program = parse_source(
        """function feed():
    hunger = 0;
end
"""
    )

    expected = "\n".join(
        [
            "#include <stdbool.h>",
            "",
            "void feed(void) {",
            "    (hunger = 0);",
            "}",
            "",
        ]
    )

    assert transpile_to_c(program) == expected


def test_transpiles_if_else_while_and_for() -> None:
    program = parse_source(
        """function main():
    if hunger > 10 then
        hunger = 10;
    else
        hunger = hunger + 1;
    end
    while true do
        tick();
    end
    for i in 0..5 do
        blink();
    end
end
"""
    )

    output = transpile_to_c(program)

    assert "if ((hunger > 10)) {" in output
    assert "} else {" in output
    assert "while (true) {" in output
    assert "for (int i = 0; i <= 5; i++) {" in output


def test_transpiles_built_in_calls() -> None:
    program = parse_source(
        """function draw():
    screen_clear();
    screen_print(0, 10, "PET");
    screen_update();
    delay_ms(1000);
end
"""
    )

    output = transpile_to_c(program)

    assert "void delay(int ms);" in output
    assert "void screen_clear(void);" in output
    assert "void screen_print(int x, int y, const char *text);" in output
    assert "void screen_update(void);" in output
    assert "screen_clear();" in output
    assert 'screen_print(0, 10, "PET");' in output
    assert "screen_update();" in output
    assert "delay(1000);" in output


def test_transpiles_console_builtins() -> None:
    program = parse_source(
        """function main():
    print("Name: ");
    let name = read_line();
    println(name);
    print(42);
    println(true);
end
"""
    )

    output = transpile_to_c(program)

    assert "void rua_print_string(const char *value);" in output
    assert "void rua_print_int(int value);" in output
    assert "void rua_println_bool(bool value);" in output
    assert "void rua_println_string(const char *value);" in output
    assert "const char *rua_read_line(void);" in output
    assert 'rua_print_string("Name: ");' in output
    assert "const char *name = rua_read_line();" in output
    assert "rua_println_string(name);" in output
    assert "rua_print_int(42);" in output
    assert "rua_println_bool(true);" in output


def test_transpiles_documented_example_program() -> None:
    program = parse_source(
        """import "arduino";
import "pet";

global hunger = 0;
global happiness = 100;
global health = 100;
global sick = false;

function feed():
    hunger = 0;
end

function tick():
    hunger = hunger + 1;
    if hunger > 10 then
        health = health - 1;
    end
end

function draw():
    screen_clear();
    screen_print(0, 0, "PET");
    screen_print(0, 10, "HUNGER");
    screen_update();
end
"""
    )

    output = transpile_to_c(program)

    assert "#include <stdbool.h>" in output
    assert "int hunger = 0;" in output
    assert "int happiness = 100;" in output
    assert "int health = 100;" in output
    assert "bool sick = false;" in output
    assert "void feed(void) {" in output
    assert "void tick(void) {" in output
    assert "void draw(void) {" in output
    assert 'screen_print(0, 0, "PET");' in output
    assert 'screen_print(0, 10, "HUNGER");' in output


def test_transpiler_writes_c_file(tmp_path: Path) -> None:
    program = parse_source("global hunger = 0;")
    output_path = tmp_path / "program.c"

    write_c(program, output_path)

    assert output_path.read_text(encoding="utf-8") == "#include <stdbool.h>\n\nint hunger = 0;\n"


def test_transpiler_instance_matches_function_api() -> None:
    program = parse_source("global hunger = 0;")
    transpiler = CTranspiler()

    assert transpiler.transpile(program) == transpile_to_c(program)
