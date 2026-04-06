# Tabela de Tokens da Linguagem Rua

Este documento resume os tokens atualmente reconhecidos pela linguagem Rua no projeto.

Cada entrada mostra:
- categoria
- regex ou padrao de reconhecimento
- exemplo de uso

## Observacoes

- Palavras-chave sao reconhecidas a partir do mesmo padrao de identificador e depois classificadas pela tabela `KEYWORDS`.
- `EOF` nao vem de um regex do codigo-fonte. Ele e adicionado pelo scanner ao final da leitura.

## Tabela de tokens

| Token | Categoria | Regex / Padrao | Exemplo de uso |
|---|---|---|---|
| `LEFT_PAREN` | Delimitador | `r"(?P<LEFT_PAREN>\()"` | `function main()` |
| `RIGHT_PAREN` | Delimitador | `r"(?P<RIGHT_PAREN>\))"` | `print(name)` |
| `COMMA` | Delimitador | `r"(?P<COMMA>,)"` | `function add(x, y)` |
| `COLON` | Delimitador de bloco | `r"(?P<COLON>:)"` | `function main():` |
| `SEMICOLON` | Terminador de statement | `r"(?P<SEMICOLON>;)"` | `global hunger = 0;` |
| `EQUAL` | Operador de atribuicao | `r"(?P<EQUAL>=)"` | `hunger = 0;` |
| `PLUS` | Operador aritmetico | `r"(?P<PLUS>\+)"` | `x + 1` |
| `MINUS` | Operador aritmetico | `r"(?P<MINUS>-)"` | `health - 1` |
| `STAR` | Operador aritmetico | `r"(?P<STAR>\*)"` | `a * b` |
| `SLASH` | Operador aritmetico | `r"(?P<SLASH>/)"` | `x / y` |
| `LESS` | Operador relacional | `r"(?P<LESS><)"` | `x < y` |
| `GREATER` | Operador relacional | `r"(?P<GREATER>>)"` | `x > y` |
| `EQUAL_EQUAL` | Operador relacional | `r"(?P<EQUAL_EQUAL>==)"` | `x == y` |
| `BANG_EQUAL` | Operador relacional | `r"(?P<BANG_EQUAL>!=)"` | `x != y` |
| `LESS_EQUAL` | Operador relacional | `r"(?P<LESS_EQUAL><=)"` | `health <= 0` |
| `GREATER_EQUAL` | Operador relacional | `r"(?P<GREATER_EQUAL>>=)"` | `score >= 10` |
| `DOT_DOT` | Operador de faixa | `r"(?P<DOT_DOT>\.\.)"` | `for i in 0..5 do` |
| `IDENTIFIER` | Identificador | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` | `hunger`, `main`, `tick` |
| `INTEGER` | Literal inteiro | `r"(?P<INTEGER>\d+)"` | `0`, `42`, `100` |
| `STRING` | Literal string | `r'(?P<STRING>"[^"\n]*")'` | `"PET"`, `"Ola"` |
| `IMPORT` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["import"]` | `import "pet";` |
| `FUNCTION` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["function"]` | `function main():` |
| `LET` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["let"]` | `let x = 1;` |
| `GLOBAL` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["global"]` | `global hunger = 0;` |
| `IF` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["if"]` | `if hunger > 10 then` |
| `THEN` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["then"]` | `if ready then` |
| `ELSE` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["else"]` | `else` |
| `WHILE` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["while"]` | `while true do` |
| `DO` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["do"]` | `while true do` |
| `FOR` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["for"]` | `for i in 0..5 do` |
| `IN` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["in"]` | `for i in 0..5 do` |
| `RETURN` | Palavra-chave | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["return"]` | `return x;` |
| `TRUE` | Literal booleano | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["true"]` | `global alive = true;` |
| `FALSE` | Literal booleano | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["false"]` | `global sick = false;` |
| `AND` | Operador logico | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["and"]` | `a and b` |
| `OR` | Operador logico | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["or"]` | `a or b` |
| `NOT` | Operador logico | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["not"]` | `not done` |
| `END` | Palavra-chave de fechamento | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["end"]` | `end` |
| `VERIFY` | Palavra-chave reservada | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["verify"]` | `verify` |
| `EXTERN` | Palavra-chave reservada | `r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)"` + `KEYWORDS["extern"]` | `extern` |
| `EOF` | Fim de arquivo | adicionado pelo scanner | fim da entrada |

## Tokens auxiliares do scanner

Os itens abaixo fazem parte do processo de varredura, mas nao viram tokens finais na lista produzida pelo scanner:

| Nome interno | Funcao | Regex / Padrao | Exemplo |
|---|---|---|---|
| `WHITESPACE` | Ignorar espacos, tabs e `\r` | `r"(?P<WHITESPACE>[ \t\r]+)"` | espacos entre palavras |
| `NEWLINE` | Avancar linha e coluna | `r"(?P<NEWLINE>\n+)"` | quebra de linha |
| `COMMENT` | Ignorar comentario de linha | `r"(?P<COMMENT>//[^\n]*)"` | `// comentario` |

# Como o Compilador Rua Funciona

Este documento mostra, de forma pratica, como o compilador Rua funciona de ponta a ponta.

A ideia e explicar:
- a estrutura geral da linguagem
- como um arquivo `.rua` e organizado
- como o compilador transforma o codigo-fonte em AST
- como a AST e usada para gerar codigo C

## 1. Estrutura da linguagem

A linguagem Rua V1 segue uma estrutura simples.
Um programa pode conter:
- imports opcionais
- declaracoes globais
- declaracoes de funcao

Nao existem comandos executaveis soltos no topo do arquivo.

A ordem esperada e:

```text
imports
globais
funcoes
```

Exemplo geral:

```rua
import "pet";

global hunger = 0;

function feed():
    hunger = 0;
end
```

## 2. Exemplo escolhido

Vamos usar exatamente estes arquivos do projeto:
- [calculator.rua](/Users/marceufilho/ibmec/compiladores-marceu/examples/calculator.rua)
- [calculator.ast.txt](/Users/marceufilho/ibmec/compiladores-marceu/out/calculator.ast.txt)
- [calculator.c](/Users/marceufilho/ibmec/compiladores-marceu/out/calculator.c)

Codigo-fonte de `calculator.rua`:

```rua
global result = 0;

function add(x, y):
    return x + y;
end

function subtract(x, y):
    return x - y;
end

function multiply(x, y):
    return x * y;
end

function divide(x, y):
    if y == 0 then
        return 0;
    end
    return x / y;
end

function max(x, y):
    if x > y then
        return x;
    end
    return y;
end

function min(x, y):
    if x < y then
        return x;
    end
    return y;
end

function main():
    let a = 20;
    let b = 5;

    result = add(a, b);
    result = subtract(result, 3);
    result = multiply(result, 2);
    result = divide(result, b);
    result = max(result, 10);
    result = min(result, 50);
end
```

Esse exemplo e melhor para entendimento porque mostra:
- declaracao global
- funcoes com parametros
- retornos com expressoes
- condicionais
- variaveis locais
- chamadas de funcao
- atribuicoes

## 3. Como o compilador processa o arquivo

O pipeline do projeto e este:

```text
arquivo .rua
-> scanner
-> tokens
-> parser
-> AST
-> impressao da AST
-> geracao de codigo C
```

Cada etapa tem um papel claro:

- o scanner reconhece tokens
- o parser reconhece a estrutura sintatica
- a AST representa o programa em arvore
- o transpiler usa a AST para gerar C

## 4. Hierarquia sintatica do exemplo

O programa `calculator.rua` tem a seguinte hierarquia sintatica:

```text
Program
├── GlobalDecl
│   ├── name: result
│   └── initializer: 0
├── FunctionDecl
│   ├── name: add
│   ├── params: [x, y]
│   └── body
│       └── ReturnStmt
├── FunctionDecl
│   ├── name: subtract
│   ├── params: [x, y]
│   └── body
│       └── ReturnStmt
├── FunctionDecl
│   ├── name: multiply
│   ├── params: [x, y]
│   └── body
│       └── ReturnStmt
├── FunctionDecl
│   ├── name: divide
│   ├── params: [x, y]
│   └── body
│       ├── IfStmt
│       └── ReturnStmt
├── FunctionDecl
│   ├── name: max
│   ├── params: [x, y]
│   └── body
│       ├── IfStmt
│       └── ReturnStmt
├── FunctionDecl
│   ├── name: min
│   ├── params: [x, y]
│   └── body
│       ├── IfStmt
│       └── ReturnStmt
└── FunctionDecl
    ├── name: main
    ├── params: []
    └── body
        ├── LocalDecl
        ├── LocalDecl
        ├── ExprStmt
        ├── ExprStmt
        ├── ExprStmt
        ├── ExprStmt
        ├── ExprStmt
        └── ExprStmt
```

Essa hierarquia mostra a estrutura principal da linguagem:
- o programa tem uma global e varias funcoes
- funcoes podem receber parametros
- algumas funcoes possuem `if` e mais de um `return`
- o corpo de `main` contem declaracoes locais e atribuicoes

## 5. AST do exemplo

Depois do parser, o codigo vira uma AST.

Usando exatamente [calculator.ast.txt](/Users/marceufilho/ibmec/compiladores-marceu/out/calculator.ast.txt), a representacao textual da AST e:

```text
Program
├── GlobalDecl
│   ├── name: 'result'
│   └── initializer: LiteralExpr(0)
├── FunctionDecl(name='add', params=['x', 'y'])
│   └── body
│       └── ReturnStmt
│           └── value: BinaryExpr
│               ├── left: VariableExpr("x")
│               ├── operator: '+'
│               └── right: VariableExpr("y")
├── FunctionDecl(name='subtract', params=['x', 'y'])
│   └── body
│       └── ReturnStmt
│           └── value: BinaryExpr
│               ├── left: VariableExpr("x")
│               ├── operator: '-'
│               └── right: VariableExpr("y")
├── FunctionDecl(name='multiply', params=['x', 'y'])
│   └── body
│       └── ReturnStmt
│           └── value: BinaryExpr
│               ├── left: VariableExpr("x")
│               ├── operator: '*'
│               └── right: VariableExpr("y")
├── FunctionDecl(name='divide', params=['x', 'y'])
│   └── body
│       ├── IfStmt
│       │   ├── condition: BinaryExpr
│       │   │   ├── left: VariableExpr("y")
│       │   │   ├── operator: '=='
│       │   │   └── right: LiteralExpr(0)
│       │   ├── then_branch
│       │   │   └── ReturnStmt
│       │   │       └── value: LiteralExpr(0)
│       │   └── else_branch: null
│       └── ReturnStmt
│           └── value: BinaryExpr
│               ├── left: VariableExpr("x")
│               ├── operator: '/'
│               └── right: VariableExpr("y")
├── FunctionDecl(name='max', params=['x', 'y'])
│   └── body
│       ├── IfStmt
│       │   ├── condition: BinaryExpr
│       │   │   ├── left: VariableExpr("x")
│       │   │   ├── operator: '>'
│       │   │   └── right: VariableExpr("y")
│       │   ├── then_branch
│       │   │   └── ReturnStmt
│       │   │       └── value: VariableExpr("x")
│       │   └── else_branch: null
│       └── ReturnStmt
│           └── value: VariableExpr("y")
├── FunctionDecl(name='min', params=['x', 'y'])
│   └── body
│       ├── IfStmt
│       │   ├── condition: BinaryExpr
│       │   │   ├── left: VariableExpr("x")
│       │   │   ├── operator: '<'
│       │   │   └── right: VariableExpr("y")
│       │   ├── then_branch
│       │   │   └── ReturnStmt
│       │   │       └── value: VariableExpr("x")
│       │   └── else_branch: null
│       └── ReturnStmt
│           └── value: VariableExpr("y")
└── FunctionDecl(name='main', params=[])
    └── body
        ├── LocalDecl
        │   ├── name: 'a'
        │   └── initializer: LiteralExpr(20)
        ├── LocalDecl
        │   ├── name: 'b'
        │   └── initializer: LiteralExpr(5)
        ├── ExprStmt
        │   └── AssignExpr
        │       ├── target: 'result'
        │       └── value: CallExpr
        │           ├── callee: VariableExpr("add")
        │           └── arguments
        │               ├── VariableExpr("a")
        │               └── VariableExpr("b")
        ├── ExprStmt
        │   └── AssignExpr
        │       ├── target: 'result'
        │       └── value: CallExpr
        │           ├── callee: VariableExpr("subtract")
        │           └── arguments
        │               ├── VariableExpr("result")
        │               └── LiteralExpr(3)
        ├── ExprStmt
        │   └── AssignExpr
        │       ├── target: 'result'
        │       └── value: CallExpr
        │           ├── callee: VariableExpr("multiply")
        │           └── arguments
        │               ├── VariableExpr("result")
        │               └── LiteralExpr(2)
        ├── ExprStmt
        │   └── AssignExpr
        │       ├── target: 'result'
        │       └── value: CallExpr
        │           ├── callee: VariableExpr("divide")
        │           └── arguments
        │               ├── VariableExpr("result")
        │               └── VariableExpr("b")
        ├── ExprStmt
        │   └── AssignExpr
        │       ├── target: 'result'
        │       └── value: CallExpr
        │           ├── callee: VariableExpr("max")
        │           └── arguments
        │               ├── VariableExpr("result")
        │               └── LiteralExpr(10)
        └── ExprStmt
            └── AssignExpr
                ├── target: 'result'
                └── value: CallExpr
                    ├── callee: VariableExpr("min")
                    └── arguments
                        ├── VariableExpr("result")
                        └── LiteralExpr(50)
```

Essa estrutura corresponde aos nos definidos em [ast_nodes.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/ast_nodes.py).

Os nos principais usados aqui sao:
- `Program`
- `GlobalDecl`
- `FunctionDecl`
- `IfStmt`
- `ReturnStmt`
- `LocalDecl`
- `AssignExpr`
- `CallExpr`

## 6. O que o parser realmente construiu

Conceitualmente, o parser monta algo equivalente a isto:

```text
Program(
  imports=[],
  globals=[
    GlobalDecl(
      name="result",
      initializer=LiteralExpr(0)
    )
  ],
  functions=[
    FunctionDecl(
      name="add",
      params=["x", "y"],
      body=[
        ReturnStmt(
          value=BinaryExpr(
            left=VariableExpr("x"),
            operator="+",
            right=VariableExpr("y")
          )
        )
      ]
    ),
    FunctionDecl(
      name="subtract",
      params=["x", "y"],
      body=[
        ReturnStmt(
          value=BinaryExpr(
            left=VariableExpr("x"),
            operator="-",
            right=VariableExpr("y")
          )
        )
      ]
    ),
    FunctionDecl(
      name="multiply",
      params=["x", "y"],
      body=[
        ReturnStmt(
          value=BinaryExpr(
            left=VariableExpr("x"),
            operator="*",
            right=VariableExpr("y")
          )
        )
      ]
    ),
    FunctionDecl(
      name="divide",
      params=["x", "y"],
      body=[
        IfStmt(
          condition=BinaryExpr(
            left=VariableExpr("y"),
            operator="==",
            right=LiteralExpr(0)
          ),
          then_branch=[ReturnStmt(value=LiteralExpr(0))],
          else_branch=None
        ),
        ReturnStmt(
          value=BinaryExpr(
            left=VariableExpr("x"),
            operator="/",
            right=VariableExpr("y")
          )
        )
      ]
    ),
    FunctionDecl(
      name="max",
      params=["x", "y"],
      body=[
        IfStmt(
          condition=BinaryExpr(
            left=VariableExpr("x"),
            operator=">",
            right=VariableExpr("y")
          ),
          then_branch=[ReturnStmt(value=VariableExpr("x"))],
          else_branch=None
        ),
        ReturnStmt(value=VariableExpr("y"))
      ]
    ),
    FunctionDecl(
      name="min",
      params=["x", "y"],
      body=[
        IfStmt(
          condition=BinaryExpr(
            left=VariableExpr("x"),
            operator="<",
            right=VariableExpr("y")
          ),
          then_branch=[ReturnStmt(value=VariableExpr("x"))],
          else_branch=None
        ),
        ReturnStmt(value=VariableExpr("y"))
      ]
    ),
    FunctionDecl(
      name="main",
      params=[],
      body=[
        LocalDecl(name="a", initializer=LiteralExpr(20)),
        LocalDecl(name="b", initializer=LiteralExpr(5)),
        ExprStmt(
          expr=AssignExpr(
            target="result",
            value=CallExpr(
              callee=VariableExpr("add"),
              arguments=[VariableExpr("a"), VariableExpr("b")]
            )
          )
        ),
        ExprStmt(
          expr=AssignExpr(
            target="result",
            value=CallExpr(
              callee=VariableExpr("subtract"),
              arguments=[VariableExpr("result"), LiteralExpr(3)]
            )
          )
        ),
        ExprStmt(
          expr=AssignExpr(
            target="result",
            value=CallExpr(
              callee=VariableExpr("multiply"),
              arguments=[VariableExpr("result"), LiteralExpr(2)]
            )
          )
        ),
        ExprStmt(
          expr=AssignExpr(
            target="result",
            value=CallExpr(
              callee=VariableExpr("divide"),
              arguments=[VariableExpr("result"), VariableExpr("b")]
            )
          )
        ),
        ExprStmt(
          expr=AssignExpr(
            target="result",
            value=CallExpr(
              callee=VariableExpr("max"),
              arguments=[VariableExpr("result"), LiteralExpr(10)]
            )
          )
        ),
        ExprStmt(
          expr=AssignExpr(
            target="result",
            value=CallExpr(
              callee=VariableExpr("min"),
              arguments=[VariableExpr("result"), LiteralExpr(50)]
            )
          )
        )
      ]
    )
  ]
)
```

Esse ponto e importante porque:
- o compilador ja nao trabalha mais com texto bruto
- ele trabalha com uma estrutura organizada
- essa estrutura facilita validacao, impressao e geracao de codigo

## 7. Codigo C gerado

O transpiler pega essa AST e produz codigo C.

Usando exatamente [calculator.c](/Users/marceufilho/ibmec/compiladores-marceu/out/calculator.c), a saida e:

```c
#include <stdbool.h>

int result = 0;

int add(int x, int y) {
    return (x + y);
}

int subtract(int x, int y) {
    return (x - y);
}

int multiply(int x, int y) {
    return (x * y);
}

int divide(int x, int y) {
    if ((y == 0)) {
        return 0;
    }
    return (x / y);
}

int max(int x, int y) {
    if ((x > y)) {
        return x;
    }
    return y;
}

int min(int x, int y) {
    if ((x < y)) {
        return x;
    }
    return y;
}

void main(void) {
    int a = 20;
    int b = 5;
    (result = add(a, b));
    (result = subtract(result, 3));
    (result = multiply(result, 2));
    (result = divide(result, b));
    (result = max(result, 10));
    (result = min(result, 50));
}
```

Esse codigo e gerado a partir da AST, nao diretamente do texto original.

## 8. Por que a AST e tao importante

A AST e o centro do compilador.

Ela e importante porque:
- separa a analise sintatica da geracao de codigo
- permite imprimir a estrutura do programa de forma legivel
- permite gerar C a partir da mesma representacao
- prepara o projeto para futuros backends e futuras analises

Hoje:
- a AST gera codigo C

No futuro:
- a AST pode alimentar um analisador semantico
- a AST pode apoiar interoperabilidade com C
- a AST pode servir como base para geracao de artefatos ligados a verificacao com Lean

## 9. Resumo final

O compilador Rua funciona assim:

1. le o arquivo `.rua`
2. reconhece tokens com o scanner
3. monta a estrutura sintatica com o parser
4. constroi a AST
5. imprime a AST em texto
6. usa a AST para gerar codigo C

Em outras palavras:

```text
fonte Rua
-> estrutura sintatica
-> AST
-> codigo C
```

Esse design deixa o projeto pequeno, claro e facil de explicar.
