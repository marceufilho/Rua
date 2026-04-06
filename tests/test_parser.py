import pytest

from rua.ast_nodes import (
    AssignExpr,
    BinaryExpr,
    CallExpr,
    ExprStmt,
    ForStmt,
    FunctionDecl,
    GlobalDecl,
    GroupingExpr,
    IfStmt,
    ImportDecl,
    LiteralExpr,
    LocalDecl,
    Program,
    ReturnStmt,
    UnaryExpr,
    VariableExpr,
    WhileStmt,
)
from rua.parser import ParseError, Parser
from rua.scanner import Scanner


def parse_source(source: str) -> Program:
    tokens = Scanner(source).scan_tokens()
    return Parser(tokens).parse()


def test_parses_minimal_valid_program() -> None:
    program = parse_source("")

    assert program == Program(imports=[], globals=[], functions=[])


def test_parses_imports_globals_and_functions() -> None:
    program = parse_source(
        """import "pet";
global hunger = 0;
function feed():
    hunger = 0;
end
"""
    )

    assert program.imports == [ImportDecl(module_name="pet")]
    assert program.globals == [GlobalDecl(name="hunger", initializer=LiteralExpr(0))]
    assert program.functions[0].name == "feed"


def test_parses_local_declarations_inside_functions() -> None:
    program = parse_source(
        """function main():
    let x = 1;
end
"""
    )

    body = program.functions[0].body
    assert body == [LocalDecl(name="x", initializer=LiteralExpr(1))]


def test_parses_if_else_statement() -> None:
    program = parse_source(
        """function tick():
    if hunger > 10 then
        hunger = 10;
    else
        hunger = hunger + 1;
    end
end
"""
    )

    if_stmt = program.functions[0].body[0]
    assert isinstance(if_stmt, IfStmt)
    assert if_stmt.condition == BinaryExpr(VariableExpr("hunger"), ">", LiteralExpr(10))
    assert if_stmt.then_branch == [ExprStmt(AssignExpr("hunger", LiteralExpr(10)))]
    assert if_stmt.else_branch == [
        ExprStmt(AssignExpr("hunger", BinaryExpr(VariableExpr("hunger"), "+", LiteralExpr(1))))
    ]


def test_parses_while_statement() -> None:
    program = parse_source(
        """function main_loop():
    while true do
        tick();
    end
end
"""
    )

    while_stmt = program.functions[0].body[0]
    assert while_stmt == WhileStmt(
        condition=LiteralExpr(True),
        body=[ExprStmt(CallExpr(callee=VariableExpr("tick"), arguments=[]))],
    )


def test_parses_bounded_for_statement() -> None:
    program = parse_source(
        """function blink_many():
    for i in 0..5 do
        blink();
    end
end
"""
    )

    for_stmt = program.functions[0].body[0]
    assert for_stmt == ForStmt(
        loop_var="i",
        start_expr=LiteralExpr(0),
        end_expr=LiteralExpr(5),
        body=[ExprStmt(CallExpr(callee=VariableExpr("blink"), arguments=[]))],
    )


def test_parses_return_without_value() -> None:
    program = parse_source(
        """function done():
    return;
end
"""
    )

    assert program.functions[0].body == [ReturnStmt(value=None)]


def test_parses_return_with_value() -> None:
    program = parse_source(
        """function max(x, y):
    return x;
end
"""
    )

    function = program.functions[0]
    assert function == FunctionDecl(name="max", params=["x", "y"], body=[ReturnStmt(value=VariableExpr("x"))])


def test_parses_expression_precedence_correctly() -> None:
    program = parse_source(
        """function calc():
    result = a + b * c and not done;
end
"""
    )

    expr_stmt = program.functions[0].body[0]
    assert expr_stmt == ExprStmt(
        expr=AssignExpr(
            target="result",
            value=BinaryExpr(
                left=BinaryExpr(
                    left=VariableExpr("a"),
                    operator="+",
                    right=BinaryExpr(left=VariableExpr("b"), operator="*", right=VariableExpr("c")),
                ),
                operator="and",
                right=UnaryExpr(operator="not", right=VariableExpr("done")),
            ),
        )
    )


def test_parses_function_calls_with_arguments() -> None:
    program = parse_source(
        """function draw():
    screen_print(0, 10, "PET");
end
"""
    )

    assert program.functions[0].body == [
        ExprStmt(
            expr=CallExpr(
                callee=VariableExpr("screen_print"),
                arguments=[LiteralExpr(0), LiteralExpr(10), LiteralExpr("PET")],
            )
        )
    ]


def test_rejects_missing_semicolon() -> None:
    with pytest.raises(ParseError, match="Expected ';' after global declaration"):
        parse_source("global hunger = 0")


def test_rejects_top_level_executable_statement() -> None:
    with pytest.raises(ParseError, match="Expected top-level declaration"):
        parse_source('print("hello");')


def test_rejects_malformed_assignment() -> None:
    with pytest.raises(ParseError, match="Invalid assignment target"):
        parse_source(
            """function bad():
    (x + 1) = 2;
end
"""
        )


def test_rejects_missing_end() -> None:
    with pytest.raises(ParseError, match="Expected 'end' after function body"):
        parse_source(
            """function broken():
    return;
"""
        )


def test_parses_nested_calls_and_grouping() -> None:
    program = parse_source(
        """function main():
    println((read_line()));
end
"""
    )

    assert program.functions[0].body == [
        ExprStmt(
            expr=CallExpr(
                callee=VariableExpr("println"),
                arguments=[GroupingExpr(expression=CallExpr(callee=VariableExpr("read_line"), arguments=[]))],
            )
        )
    ]
