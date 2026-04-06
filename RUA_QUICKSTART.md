# RUA: the ugly sibling of Lua and long-distance cousin of Go

Rua is a small imperative language for simple programs.

It is designed to be:
- easy to read
- easy to parse
- easy to compile

If you are new to Rua, this guide shows the main parts of the language so you can start writing code quickly.

## Program structure

A Rua program is made of:
- optional `import` declarations
- optional `global` declarations
- function declarations

Top-level executable statements are not allowed.

```rua
import "pet";

global hunger = 0;

function feed():
    hunger = 0;
end
```

## The `main` function

Most programs are built around a `main` function.

```rua
function main():
    print("hello");
end
```

This is the usual entry point for a program, but it is not required for the file to compile. Rua can compile any valid set of declarations and functions.

## Variables

Use `global` for global variables and `let` for local variables.

```rua
global score = 0;

function play():
    let bonus = 10;
    score = score + bonus;
end
```

All variables are mutable.

## Values

Rua has three basic kinds of values:
- `int`
- `bool`
- `string`

Examples:

```rua
let n = 42;
let ready = true;
let name = "Rua";
```

## Functions

Functions are declared with `function`.

```rua
function add(x, y):
    return x + y;
end
```

Functions may:
- take parameters
- return a value
- return nothing

```rua
function done():
    return;
end
```

## Assignment and expressions

Rua supports basic arithmetic and boolean expressions.

```rua
let x = 10;
let y = 5;
let result = x + y * 2;
let ok = result > 10 and not false;
```

Supported operators include:
- `+`, `-`, `*`, `/`
- `==`, `!=`, `<`, `<=`, `>`, `>=`
- `and`, `or`, `not`

## If statements

Use `if`, `then`, `else`, and `end`.

```rua
function check():
    if score > 100 then
        print("great");
    else
        print("keep going");
    end
end
```

## While loops

Use `while` with `do` and `end`.

```rua
function countdown():
    let n = 3;
    while n > 0 do
        println(n);
        n = n - 1;
    end
end
```

## For loops

Rua supports bounded range loops with `..`.

```rua
function show_numbers():
    for i in 1..5 do
        println(i);
    end
end
```

## Function calls

Function calls can appear as expressions or as standalone statements.

```rua
function main():
    let total = add(2, 3);
    println(total);
end
```

## Built-in functions

Rua currently includes simple built-ins such as:
- `print(value)`
- `println(value)`
- `read_line()`

Example:

```rua
function main():
    print("What is your name? ");
    let name = read_line();
    println(name);
end
```

Some examples in the project also use embedded-style built-ins like:
- `screen_clear()`
- `screen_print(x, y, text)`
- `screen_update()`
- `delay_ms(ms)`

## Comments

Rua uses `//` for line comments.

```rua
// increase score
score = score + 1;
```

## A small complete example

```rua
global result = 0;

function add(x, y):
    return x + y;
end

function main():
    let a = 20;
    let b = 5;
    result = add(a, b);
    println(result);
end
```

## Summary

Rua keeps the language small on purpose.

The core ideas are:
- globals and locals
- functions
- expressions
- `if`
- `while`
- bounded `for`
- simple built-ins

That is enough to start writing small programs and enough to understand how the compiler works.
