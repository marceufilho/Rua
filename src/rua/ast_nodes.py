from __future__ import annotations

from dataclasses import dataclass


class Node:
    """Base type for all AST nodes."""


class Decl(Node):
    """Base type for declaration nodes."""


class Stmt(Node):
    """Base type for statement nodes."""


class Expr(Node):
    """Base type for expression nodes."""


DeclOrStmt = Decl | Stmt


@dataclass(frozen=True, slots=True)
class Program(Node):
    imports: list[ImportDecl]
    globals: list[GlobalDecl]
    functions: list[FunctionDecl]


@dataclass(frozen=True, slots=True)
class ImportDecl(Decl):
    module_name: str


@dataclass(frozen=True, slots=True)
class GlobalDecl(Decl):
    name: str
    initializer: Expr


@dataclass(frozen=True, slots=True)
class LocalDecl(Decl):
    name: str
    initializer: Expr


@dataclass(frozen=True, slots=True)
class FunctionDecl(Decl):
    name: str
    params: list[str]
    body: list[DeclOrStmt]


@dataclass(frozen=True, slots=True)
class IfStmt(Stmt):
    condition: Expr
    then_branch: list[DeclOrStmt]
    else_branch: list[DeclOrStmt] | None


@dataclass(frozen=True, slots=True)
class WhileStmt(Stmt):
    condition: Expr
    body: list[DeclOrStmt]


@dataclass(frozen=True, slots=True)
class ForStmt(Stmt):
    loop_var: str
    start_expr: Expr
    end_expr: Expr
    body: list[DeclOrStmt]


@dataclass(frozen=True, slots=True)
class ReturnStmt(Stmt):
    value: Expr | None


@dataclass(frozen=True, slots=True)
class ExprStmt(Stmt):
    expr: Expr


@dataclass(frozen=True, slots=True)
class LiteralExpr(Expr):
    value: object


@dataclass(frozen=True, slots=True)
class VariableExpr(Expr):
    name: str


@dataclass(frozen=True, slots=True)
class GroupingExpr(Expr):
    expression: Expr


@dataclass(frozen=True, slots=True)
class UnaryExpr(Expr):
    operator: str
    right: Expr


@dataclass(frozen=True, slots=True)
class BinaryExpr(Expr):
    left: Expr
    operator: str
    right: Expr


@dataclass(frozen=True, slots=True)
class AssignExpr(Expr):
    target: str
    value: Expr


@dataclass(frozen=True, slots=True)
class CallExpr(Expr):
    callee: Expr
    arguments: list[Expr]
