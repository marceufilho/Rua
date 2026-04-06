"""Simple C transpiler for Rua V1 AST nodes."""

from pathlib import Path

from rua.ast_nodes import (
    AssignExpr,
    BinaryExpr,
    CallExpr,
    Decl,
    Expr,
    ExprStmt,
    ForStmt,
    FunctionDecl,
    GlobalDecl,
    GroupingExpr,
    IfStmt,
    LiteralExpr,
    LocalDecl,
    Program,
    ReturnStmt,
    Stmt,
    UnaryExpr,
    VariableExpr,
    WhileStmt,
)


class CTranspiler:
    """Transpile Rua AST nodes into simple readable C code."""

    BUILTIN_CALLS = {
        "delay_ms": "delay",
        "millis": "millis",
        "button_pressed": "button_pressed",
        "screen_clear": "screen_clear",
        "screen_print": "screen_print",
        "screen_update": "screen_update",
        "read_line": "rua_read_line",
    }

    BUILTIN_PROTOTYPES = {
        "delay": "void delay(int ms);",
        "millis": "int millis(void);",
        "button_pressed": "bool button_pressed(int btn);",
        "screen_clear": "void screen_clear(void);",
        "screen_print": "void screen_print(int x, int y, const char *text);",
        "screen_update": "void screen_update(void);",
        "rua_print_int": "void rua_print_int(int value);",
        "rua_print_bool": "void rua_print_bool(bool value);",
        "rua_print_string": "void rua_print_string(const char *value);",
        "rua_println_int": "void rua_println_int(int value);",
        "rua_println_bool": "void rua_println_bool(bool value);",
        "rua_println_string": "void rua_println_string(const char *value);",
        "rua_read_line": "const char *rua_read_line(void);",
    }

    def __init__(self) -> None:
        self.global_types: dict[str, str] = {}

    def transpile(self, program: Program) -> str:
        lines = ["#include <stdbool.h>"]
        self.global_types = {
            global_decl.name: self._infer_expr_type(global_decl.initializer, {}) for global_decl in program.globals
        }

        builtins = self._collect_builtin_names(program)
        if builtins:
            lines.append("")
            for builtin_name in sorted(builtins):
                lines.append(self.BUILTIN_PROTOTYPES[builtin_name])

        if program.globals:
            lines.append("")
            for global_decl in program.globals:
                lines.append(self._transpile_global(global_decl))

        if program.functions:
            for function in program.functions:
                lines.append("")
                lines.extend(self._transpile_function(function))

        return "\n".join(lines) + "\n"

    def write(self, program: Program, output_path: str | Path) -> None:
        Path(output_path).write_text(self.transpile(program), encoding="utf-8")

    def _transpile_global(self, decl: GlobalDecl) -> str:
        c_type = self._infer_expr_type(decl.initializer, self.global_types)
        value = self._transpile_expr(decl.initializer, self.global_types)
        return f"{self._format_declaration(c_type, decl.name)} = {value};"

    def _transpile_function(self, function: FunctionDecl) -> list[str]:
        variable_types = dict(self.global_types)
        for param in function.params:
            variable_types[param] = "int"

        return_type = self._infer_function_return_type(function, variable_types)
        params = ", ".join(f"int {param}" for param in function.params) or "void"
        lines = [f"{return_type} {function.name}({params}) {{"]
        lines.extend(self._transpile_block(function.body, indent=1, variable_types=variable_types))
        lines.append("}")
        return lines

    def _transpile_block(self, items: list[Decl | Stmt], indent: int, variable_types: dict[str, str]) -> list[str]:
        lines: list[str] = []
        for item in items:
            lines.extend(self._transpile_item(item, indent, variable_types))
        return lines

    def _transpile_item(self, item: Decl | Stmt, indent: int, variable_types: dict[str, str]) -> list[str]:
        prefix = "    " * indent

        if isinstance(item, LocalDecl):
            c_type = self._infer_expr_type(item.initializer, variable_types)
            variable_types[item.name] = c_type
            value = self._transpile_expr(item.initializer, variable_types)
            return [f"{prefix}{self._format_declaration(c_type, item.name)} = {value};"]

        if isinstance(item, ExprStmt):
            return [f"{prefix}{self._transpile_expr(item.expr, variable_types)};"]

        if isinstance(item, IfStmt):
            lines = [f"{prefix}if ({self._transpile_expr(item.condition, variable_types)}) {{"]
            lines.extend(self._transpile_block(item.then_branch, indent + 1, dict(variable_types)))
            if item.else_branch is None:
                lines.append(f"{prefix}}}")
                return lines

            lines.append(f"{prefix}}} else {{")
            lines.extend(self._transpile_block(item.else_branch, indent + 1, dict(variable_types)))
            lines.append(f"{prefix}}}")
            return lines

        if isinstance(item, WhileStmt):
            lines = [f"{prefix}while ({self._transpile_expr(item.condition, variable_types)}) {{"]
            lines.extend(self._transpile_block(item.body, indent + 1, dict(variable_types)))
            lines.append(f"{prefix}}}")
            return lines

        if isinstance(item, ForStmt):
            start = self._transpile_expr(item.start_expr, variable_types)
            end = self._transpile_expr(item.end_expr, variable_types)
            loop_types = dict(variable_types)
            loop_types[item.loop_var] = "int"
            lines = [f"{prefix}for (int {item.loop_var} = {start}; {item.loop_var} <= {end}; {item.loop_var}++) {{"]
            lines.extend(self._transpile_block(item.body, indent + 1, loop_types))
            lines.append(f"{prefix}}}")
            return lines

        if isinstance(item, ReturnStmt):
            if item.value is None:
                return [f"{prefix}return;"]
            return [f"{prefix}return {self._transpile_expr(item.value, variable_types)};"]

        raise TypeError(f"Unsupported AST item: {type(item).__name__}")

    def _transpile_expr(self, expr: Expr, variable_types: dict[str, str]) -> str:
        if isinstance(expr, LiteralExpr):
            return self._transpile_literal(expr.value)
        if isinstance(expr, VariableExpr):
            return expr.name
        if isinstance(expr, GroupingExpr):
            return f"({self._transpile_expr(expr.expression, variable_types)})"
        if isinstance(expr, UnaryExpr):
            operator = "!" if expr.operator == "not" else expr.operator
            return f"({operator}{self._transpile_expr(expr.right, variable_types)})"
        if isinstance(expr, BinaryExpr):
            operator = self._map_binary_operator(expr.operator)
            left = self._transpile_expr(expr.left, variable_types)
            right = self._transpile_expr(expr.right, variable_types)
            return f"({left} {operator} {right})"
        if isinstance(expr, AssignExpr):
            return f"({expr.target} = {self._transpile_expr(expr.value, variable_types)})"
        if isinstance(expr, CallExpr):
            if isinstance(expr.callee, VariableExpr):
                if expr.callee.name in {"print", "println"}:
                    return self._transpile_print_call(expr, variable_types)
                callee = self.BUILTIN_CALLS.get(expr.callee.name, expr.callee.name)
            else:
                callee = self._transpile_expr(expr.callee, variable_types)
            arguments = ", ".join(self._transpile_expr(argument, variable_types) for argument in expr.arguments)
            return f"{callee}({arguments})"
        raise TypeError(f"Unsupported expression: {type(expr).__name__}")

    def _infer_function_return_type(self, function: FunctionDecl, variable_types: dict[str, str]) -> str:
        for item in function.body:
            if isinstance(item, LocalDecl):
                variable_types[item.name] = self._infer_expr_type(item.initializer, variable_types)
            if isinstance(item, ReturnStmt) and item.value is not None:
                return self._infer_expr_type(item.value, variable_types)
        return "void"

    def _infer_expr_type(self, expr: Expr, variable_types: dict[str, str]) -> str:
        if isinstance(expr, LiteralExpr):
            if isinstance(expr.value, bool):
                return "bool"
            if isinstance(expr.value, int):
                return "int"
            if isinstance(expr.value, str):
                return "const char *"
        if isinstance(expr, VariableExpr):
            return variable_types.get(expr.name, self.global_types.get(expr.name, "int"))
        if isinstance(expr, UnaryExpr) and expr.operator == "not":
            return "bool"
        if isinstance(expr, BinaryExpr):
            if expr.operator in {"==", "!=", "<", "<=", ">", ">=", "and", "or"}:
                return "bool"
            return self._infer_expr_type(expr.left, variable_types)
        if isinstance(expr, GroupingExpr):
            return self._infer_expr_type(expr.expression, variable_types)
        if isinstance(expr, AssignExpr):
            return self._infer_expr_type(expr.value, variable_types)
        if isinstance(expr, CallExpr):
            return self._infer_call_type(expr)
        return "int"

    def _infer_call_type(self, expr: CallExpr) -> str:
        if isinstance(expr.callee, VariableExpr):
            if expr.callee.name == "button_pressed":
                return "bool"
            if expr.callee.name == "millis":
                return "int"
            if expr.callee.name == "read_line":
                return "const char *"
        return "int"

    def _collect_builtin_names(self, program: Program) -> set[str]:
        builtins: set[str] = set()

        def visit_expr(expr: Expr, variable_types: dict[str, str]) -> None:
            if isinstance(expr, (LiteralExpr, VariableExpr)):
                return
            if isinstance(expr, GroupingExpr):
                visit_expr(expr.expression, variable_types)
                return
            if isinstance(expr, UnaryExpr):
                visit_expr(expr.right, variable_types)
                return
            if isinstance(expr, BinaryExpr):
                visit_expr(expr.left, variable_types)
                visit_expr(expr.right, variable_types)
                return
            if isinstance(expr, AssignExpr):
                visit_expr(expr.value, variable_types)
                return
            if isinstance(expr, CallExpr):
                if isinstance(expr.callee, VariableExpr):
                    if expr.callee.name in {"print", "println"}:
                        builtins.add(self._print_helper_name(expr.callee.name, expr.arguments, variable_types))
                    else:
                        mapped = self.BUILTIN_CALLS.get(expr.callee.name)
                        if mapped is not None:
                            builtins.add(mapped)
                visit_expr(expr.callee, variable_types)
                for argument in expr.arguments:
                    visit_expr(argument, variable_types)

        def visit_item(item: Decl | Stmt, variable_types: dict[str, str]) -> None:
            if isinstance(item, (GlobalDecl, LocalDecl)):
                visit_expr(item.initializer, variable_types)
                variable_types[item.name] = self._infer_expr_type(item.initializer, variable_types)
                return
            if isinstance(item, ExprStmt):
                visit_expr(item.expr, variable_types)
                return
            if isinstance(item, IfStmt):
                visit_expr(item.condition, variable_types)
                for branch_item in item.then_branch:
                    visit_item(branch_item, dict(variable_types))
                if item.else_branch is not None:
                    for branch_item in item.else_branch:
                        visit_item(branch_item, dict(variable_types))
                return
            if isinstance(item, WhileStmt):
                visit_expr(item.condition, variable_types)
                for body_item in item.body:
                    visit_item(body_item, dict(variable_types))
                return
            if isinstance(item, ForStmt):
                visit_expr(item.start_expr, variable_types)
                visit_expr(item.end_expr, variable_types)
                loop_types = dict(variable_types)
                loop_types[item.loop_var] = "int"
                for body_item in item.body:
                    visit_item(body_item, loop_types)
                return
            if isinstance(item, ReturnStmt) and item.value is not None:
                visit_expr(item.value, variable_types)

        for global_decl in program.globals:
            visit_item(global_decl, dict(self.global_types))
        for function in program.functions:
            variable_types = dict(self.global_types)
            for param in function.params:
                variable_types[param] = "int"
            for item in function.body:
                visit_item(item, variable_types)

        return builtins

    @staticmethod
    def _map_binary_operator(operator: str) -> str:
        if operator == "and":
            return "&&"
        if operator == "or":
            return "||"
        return operator

    def _transpile_print_call(self, expr: CallExpr, variable_types: dict[str, str]) -> str:
        callee_name = expr.callee.name
        helper_name = self._print_helper_name(callee_name, expr.arguments, variable_types)
        arguments = ", ".join(self._transpile_expr(argument, variable_types) for argument in expr.arguments)
        return f"{helper_name}({arguments})"

    def _print_helper_name(self, callee_name: str, arguments: list[Expr], variable_types: dict[str, str]) -> str:
        prefix = "rua_println" if callee_name == "println" else "rua_print"
        suffix = self._print_type_suffix(arguments[0], variable_types) if arguments else "int"
        return f"{prefix}_{suffix}"

    def _print_type_suffix(self, expr: Expr, variable_types: dict[str, str]) -> str:
        c_type = self._infer_expr_type(expr, variable_types)
        if c_type == "bool":
            return "bool"
        if c_type == "const char *":
            return "string"
        return "int"

    @staticmethod
    def _transpile_literal(value: object) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, str):
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        return repr(value)

    @staticmethod
    def _format_declaration(c_type: str, name: str) -> str:
        if c_type.endswith("*"):
            return f"{c_type}{name}"
        return f"{c_type} {name}"


def transpile_to_c(program: Program) -> str:
    """Transpile a Rua AST program into C source code."""
    return CTranspiler().transpile(program)


def write_c(program: Program, output_path: str | Path) -> None:
    """Write transpiled C source code to a file."""
    CTranspiler().write(program, output_path)
