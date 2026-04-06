from pathlib import Path

from rua.ast_nodes import (
    AssignExpr,
    BinaryExpr,
    ExprStmt,
    IfStmt,
    ImportDecl,
    LiteralExpr,
    Program,
    VariableExpr,
)
from rua.ast_printer import AstPrinter, format_ast, write_ast
from rua.parser import Parser
from rua.scanner import Scanner


def parse_source(source: str) -> Program:
    return Parser(Scanner(source).scan_tokens()).parse()


def test_prints_simple_assignment_ast() -> None:
    node = ExprStmt(
        expr=AssignExpr(
            target="hunger",
            value=BinaryExpr(
                left=VariableExpr("hunger"),
                operator="+",
                right=LiteralExpr(1),
            ),
        )
    )

    expected = "\n".join(
        [
            "ExprStmt",
            "└── AssignExpr",
            "    ├── target: 'hunger'",
            "    └── value: BinaryExpr",
            '        ├── left: VariableExpr("hunger")',
            "        ├── operator: '+'",
            "        └── right: LiteralExpr(1)",
        ]
    )

    assert format_ast(node) == expected


def test_prints_if_statement_ast() -> None:
    node = IfStmt(
        condition=BinaryExpr(
            left=VariableExpr("hunger"),
            operator=">",
            right=LiteralExpr(10),
        ),
        then_branch=[ExprStmt(expr=AssignExpr(target="hunger", value=LiteralExpr(10)))],
        else_branch=None,
    )

    expected = "\n".join(
        [
            "IfStmt",
            "├── condition: BinaryExpr",
            '│   ├── left: VariableExpr("hunger")',
            "│   ├── operator: '>'",
            "│   └── right: LiteralExpr(10)",
            "├── then_branch",
            "│   └── ExprStmt",
            "│       └── AssignExpr",
            "│           ├── target: 'hunger'",
            "│           └── value: LiteralExpr(10)",
            "└── else_branch: null",
        ]
    )

    assert format_ast(node) == expected


def test_prints_full_small_program_ast() -> None:
    program = parse_source(
        """import "pet";

global hunger = 0;

function feed():
    hunger = 0;
end
"""
    )

    expected = "\n".join(
        [
            "Program",
            '├── ImportDecl(module_name="pet")',
            "├── GlobalDecl",
            "│   ├── name: 'hunger'",
            "│   └── initializer: LiteralExpr(0)",
            "└── FunctionDecl(name='feed', params=[])",
            "    └── body",
            "        └── ExprStmt",
            "            └── AssignExpr",
            "                ├── target: 'hunger'",
            "                └── value: LiteralExpr(0)",
        ]
    )

    assert format_ast(program) == expected


def test_writes_ast_to_text_file(tmp_path: Path) -> None:
    program = Program(imports=[ImportDecl(module_name="pet")], globals=[], functions=[])
    output_path = tmp_path / "program.ast.txt"

    write_ast(program, output_path)

    assert output_path.read_text(encoding="utf-8") == 'Program\n└── ImportDecl(module_name="pet")\n'


def test_ast_printer_instance_matches_function_api() -> None:
    program = Program(imports=[ImportDecl(module_name="pet")], globals=[], functions=[])
    printer = AstPrinter()

    assert printer.format(program) == format_ast(program)
