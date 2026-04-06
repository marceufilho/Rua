"""Readable AST formatting for Rua V1 nodes."""

from pathlib import Path

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
    Node,
    Program,
    ReturnStmt,
    UnaryExpr,
    VariableExpr,
    WhileStmt,
)


class AstPrinter:
    """Format Rua AST nodes as a stable tree string."""

    def format(self, node: Node) -> str:
        lines = [self._node_label(node)]
        children = self._children(node)
        for index, child in enumerate(children):
            lines.extend(self._format_child(child, "", index == len(children) - 1))
        return "\n".join(lines)

    def write(self, node: Node, output_path: str | Path) -> None:
        Path(output_path).write_text(f"{self.format(node)}\n", encoding="utf-8")

    def _format_node(self, node: Node, prefix: str, is_last: bool) -> list[str]:
        branch = "└── " if is_last else "├── "
        line = f"{prefix}{branch}{self._node_label(node)}"
        child_prefix = prefix + ("    " if is_last else "│   ")

        children = self._children(node)
        lines = [line]
        for index, child in enumerate(children):
            child_is_last = index == len(children) - 1
            lines.extend(self._format_child(child, child_prefix, child_is_last))
        return lines

    def _format_child(self, child: object, prefix: str, is_last: bool) -> list[str]:
        branch = "└── " if is_last else "├── "

        if isinstance(child, tuple):
            name, value = child
            if isinstance(value, Node):
                lines = [f"{prefix}{branch}{name}: {self._node_label(value)}"]
                nested_prefix = prefix + ("    " if is_last else "│   ")
                grandchildren = self._children(value)
                for index, grandchild in enumerate(grandchildren):
                    lines.extend(
                        self._format_child(
                            grandchild,
                            nested_prefix,
                            index == len(grandchildren) - 1,
                        )
                    )
                return lines

            if isinstance(value, list):
                lines = [f"{prefix}{branch}{name}"]
                nested_prefix = prefix + ("    " if is_last else "│   ")
                if not value:
                    lines.append(f"{nested_prefix}└── []")
                    return lines
                for index, item in enumerate(value):
                    lines.extend(self._format_child(item, nested_prefix, index == len(value) - 1))
                return lines

            return [f"{prefix}{branch}{name}: {self._format_scalar(value)}"]

        return self._format_node(child, prefix, is_last)

    def _node_label(self, node: Node) -> str:
        if isinstance(node, ImportDecl):
            return f'ImportDecl(module_name="{node.module_name}")'
        if isinstance(node, FunctionDecl):
            return f"FunctionDecl(name={self._format_scalar(node.name)}, params={node.params!r})"
        if isinstance(node, LiteralExpr):
            return f"LiteralExpr({self._format_scalar(node.value)})"
        if isinstance(node, VariableExpr):
            return f'VariableExpr("{node.name}")'
        return type(node).__name__

    def _children(self, node: Node) -> list[object]:
        if isinstance(node, Program):
            return [*node.imports, *node.globals, *node.functions]
        if isinstance(node, GlobalDecl):
            return [("name", node.name), ("initializer", node.initializer)]
        if isinstance(node, LocalDecl):
            return [("name", node.name), ("initializer", node.initializer)]
        if isinstance(node, FunctionDecl):
            return [("body", node.body)]
        if isinstance(node, IfStmt):
            return [
                ("condition", node.condition),
                ("then_branch", node.then_branch),
                ("else_branch", node.else_branch),
            ]
        if isinstance(node, WhileStmt):
            return [("condition", node.condition), ("body", node.body)]
        if isinstance(node, ForStmt):
            return [
                ("loop_var", node.loop_var),
                ("start_expr", node.start_expr),
                ("end_expr", node.end_expr),
                ("body", node.body),
            ]
        if isinstance(node, ReturnStmt):
            return [("value", node.value)]
        if isinstance(node, ExprStmt):
            return [node.expr]
        if isinstance(node, GroupingExpr):
            return [("expression", node.expression)]
        if isinstance(node, UnaryExpr):
            return [("operator", node.operator), ("right", node.right)]
        if isinstance(node, BinaryExpr):
            return [("left", node.left), ("operator", node.operator), ("right", node.right)]
        if isinstance(node, AssignExpr):
            return [("target", node.target), ("value", node.value)]
        if isinstance(node, CallExpr):
            return [("callee", node.callee), ("arguments", node.arguments)]
        return []

    @staticmethod
    def _format_scalar(value: object) -> str:
        if value is None:
            return "null"
        return repr(value)


def format_ast(node: Node) -> str:
    """Format a Rua AST node as a readable tree string."""
    return AstPrinter().format(node)


def write_ast(node: Node, output_path: str | Path) -> None:
    """Write a formatted Rua AST tree to a text file."""
    AstPrinter().write(node, output_path)
