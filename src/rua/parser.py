"""Recursive-descent parser for Rua V1."""

from rua.ast_nodes import (
    AssignExpr,
    BinaryExpr,
    CallExpr,
    Expr,
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
from rua.tokens import Token, TokenType


class ParseError(Exception):
    """Raised when the parser finds invalid token structure."""


class Parser:
    """Parse a sequence of tokens into Rua AST nodes."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        imports: list[ImportDecl] = []
        globals_: list[GlobalDecl] = []
        functions: list[FunctionDecl] = []

        while self.match(TokenType.IMPORT):
            imports.append(self.import_decl())

        while self.match(TokenType.GLOBAL):
            globals_.append(self.global_decl())

        while self.match(TokenType.FUNCTION):
            functions.append(self.function_decl())

        if not self.check(TokenType.EOF):
            self.error_at(self.peek(), "Expected top-level declaration.")

        self.consume(TokenType.EOF, "Expected end of file.")
        return Program(imports=imports, globals=globals_, functions=functions)

    def import_decl(self) -> ImportDecl:
        module_name = self.consume(TokenType.STRING, "Expected module string after 'import'.")
        self.consume(TokenType.SEMICOLON, "Expected ';' after import declaration.")
        return ImportDecl(module_name=str(module_name.literal))

    def global_decl(self) -> GlobalDecl:
        name = self.consume(TokenType.IDENTIFIER, "Expected global variable name.")
        self.consume(TokenType.EQUAL, "Expected '=' after global variable name.")
        initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after global declaration.")
        return GlobalDecl(name=name.lexeme, initializer=initializer)

    def function_decl(self) -> FunctionDecl:
        name = self.consume(TokenType.IDENTIFIER, "Expected function name.")
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after function name.")

        params: list[str] = []
        if not self.check(TokenType.RIGHT_PAREN):
            params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name.").lexeme)
            while self.match(TokenType.COMMA):
                params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name.").lexeme)

        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after function parameters.")
        self.consume(TokenType.COLON, "Expected ':' before function body.")
        body = self.block({TokenType.END})
        self.consume(TokenType.END, "Expected 'end' after function body.")
        return FunctionDecl(name=name.lexeme, params=params, body=body)

    def block(
        self, stop_types: set[TokenType]
    ) -> list[LocalDecl | ExprStmt | IfStmt | WhileStmt | ForStmt | ReturnStmt]:
        items = []
        while not self.check_any(stop_types) and not self.is_at_end():
            items.append(self.declaration())
        return items

    def declaration(self) -> LocalDecl | ExprStmt | IfStmt | WhileStmt | ForStmt | ReturnStmt:
        if self.match(TokenType.LET):
            return self.local_decl()
        return self.statement()

    def local_decl(self) -> LocalDecl:
        name = self.consume(TokenType.IDENTIFIER, "Expected local variable name.")
        self.consume(TokenType.EQUAL, "Expected '=' after local variable name.")
        initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after local declaration.")
        return LocalDecl(name=name.lexeme, initializer=initializer)

    def statement(self) -> ExprStmt | IfStmt | WhileStmt | ForStmt | ReturnStmt:
        if self.match(TokenType.IF):
            return self.if_stmt()
        if self.match(TokenType.WHILE):
            return self.while_stmt()
        if self.match(TokenType.FOR):
            return self.for_stmt()
        if self.match(TokenType.RETURN):
            return self.return_stmt()
        return self.expr_stmt()

    def if_stmt(self) -> IfStmt:
        condition = self.expression()
        self.consume(TokenType.THEN, "Expected 'then' after if condition.")
        then_branch = self.block({TokenType.ELSE, TokenType.END})

        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.block({TokenType.END})

        self.consume(TokenType.END, "Expected 'end' after if statement.")
        return IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def while_stmt(self) -> WhileStmt:
        condition = self.expression()
        self.consume(TokenType.DO, "Expected 'do' after while condition.")
        body = self.block({TokenType.END})
        self.consume(TokenType.END, "Expected 'end' after while loop.")
        return WhileStmt(condition=condition, body=body)

    def for_stmt(self) -> ForStmt:
        loop_var = self.consume(TokenType.IDENTIFIER, "Expected loop variable name.")
        self.consume(TokenType.IN, "Expected 'in' after loop variable.")
        start_expr = self.expression()
        self.consume(TokenType.DOT_DOT, "Expected '..' in for range.")
        end_expr = self.expression()
        self.consume(TokenType.DO, "Expected 'do' after for range.")
        body = self.block({TokenType.END})
        self.consume(TokenType.END, "Expected 'end' after for loop.")
        return ForStmt(loop_var=loop_var.lexeme, start_expr=start_expr, end_expr=end_expr, body=body)

    def return_stmt(self) -> ReturnStmt:
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after return statement.")
        return ReturnStmt(value=value)

    def expr_stmt(self) -> ExprStmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return ExprStmt(expr=expr)

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.logic_or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, VariableExpr):
                return AssignExpr(target=expr.name, value=value)
            self.error_at(equals, "Invalid assignment target.")

        return expr

    def logic_or(self) -> Expr:
        expr = self.logic_and()
        while self.match(TokenType.OR):
            operator = self.previous().lexeme
            right = self.logic_and()
            expr = BinaryExpr(left=expr, operator=operator, right=right)
        return expr

    def logic_and(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous().lexeme
            right = self.equality()
            expr = BinaryExpr(left=expr, operator=operator, right=right)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous().lexeme
            right = self.comparison()
            expr = BinaryExpr(left=expr, operator=operator, right=right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            operator = self.previous().lexeme
            right = self.term()
            expr = BinaryExpr(left=expr, operator=operator, right=right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().lexeme
            right = self.factor()
            expr = BinaryExpr(left=expr, operator=operator, right=right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous().lexeme
            right = self.unary()
            expr = BinaryExpr(left=expr, operator=operator, right=right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.previous().lexeme
            right = self.unary()
            return UnaryExpr(operator=operator, right=right)
        return self.call()

    def call(self) -> Expr:
        expr = self.primary()
        while self.match(TokenType.LEFT_PAREN):
            arguments: list[Expr] = []
            if not self.check(TokenType.RIGHT_PAREN):
                arguments.append(self.expression())
                while self.match(TokenType.COMMA):
                    arguments.append(self.expression())
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after function arguments.")
            expr = CallExpr(callee=expr, arguments=arguments)
        return expr

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return LiteralExpr(False)
        if self.match(TokenType.TRUE):
            return LiteralExpr(True)
        if self.match(TokenType.INTEGER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return VariableExpr(self.previous().lexeme)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return GroupingExpr(expr)
        self.error_at(self.peek(), "Expected expression.")

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        self.error_at(self.peek(), message)

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return token_type is TokenType.EOF
        return self.peek().type is token_type

    def check_any(self, token_types: set[TokenType]) -> bool:
        return self.peek().type in token_types

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type is TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def error_at(self, token: Token, message: str) -> None:
        token_name = "end of file" if token.type is TokenType.EOF else repr(token.lexeme)
        raise ParseError(f"{message} At {token_name}, line {token.line}, column {token.column}.")
