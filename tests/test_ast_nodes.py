from dataclasses import fields

from rua.ast_nodes import (
    AssignExpr,
    BinaryExpr,
    ExprStmt,
    FunctionDecl,
    GlobalDecl,
    IfStmt,
    ImportDecl,
    LiteralExpr,
    LocalDecl,
    Program,
    ReturnStmt,
    VariableExpr,
    WhileStmt,
)


def test_program_node_matches_spec_shape() -> None:
    program = Program(
        imports=[ImportDecl(module_name="pet")],
        globals=[GlobalDecl(name="hunger", initializer=LiteralExpr(0))],
        functions=[
            FunctionDecl(
                name="feed",
                params=[],
                body=[ExprStmt(expr=AssignExpr(target="hunger", value=LiteralExpr(0)))],
            )
        ],
    )

    assert program.imports[0].module_name == "pet"
    assert program.globals[0].name == "hunger"
    assert program.functions[0].name == "feed"
    assert isinstance(program.functions[0].body[0], ExprStmt)


def test_control_flow_nodes_hold_decl_or_stmt_lists() -> None:
    local_decl = LocalDecl(name="x", initializer=LiteralExpr(1))
    assignment = ExprStmt(expr=AssignExpr(target="x", value=LiteralExpr(2)))

    if_stmt = IfStmt(
        condition=VariableExpr("ready"),
        then_branch=[local_decl, assignment],
        else_branch=None,
    )
    while_stmt = WhileStmt(condition=VariableExpr("running"), body=[assignment])

    assert if_stmt.then_branch == [local_decl, assignment]
    assert if_stmt.else_branch is None
    assert while_stmt.body == [assignment]


def test_expression_nodes_preserve_operator_structure() -> None:
    expr = BinaryExpr(
        left=VariableExpr("hunger"),
        operator="+",
        right=LiteralExpr(1),
    )
    return_stmt = ReturnStmt(value=expr)

    assert return_stmt.value == expr
    assert expr.left == VariableExpr("hunger")
    assert expr.operator == "+"
    assert expr.right == LiteralExpr(1)


def test_spec_field_names_match_expected_api() -> None:
    assert [field.name for field in fields(ImportDecl)] == ["module_name"]
    assert [field.name for field in fields(GlobalDecl)] == ["name", "initializer"]
    assert [field.name for field in fields(LocalDecl)] == ["name", "initializer"]
    assert [field.name for field in fields(FunctionDecl)] == ["name", "params", "body"]
    assert [field.name for field in fields(IfStmt)] == ["condition", "then_branch", "else_branch"]
