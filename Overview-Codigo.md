# Visao Geral para Desenvolvedores

Este documento explica como o projeto Rua esta organizado hoje.

Ele foi feito para desenvolvedores que querem:
- entender o pipeline atual do compilador
- navegar pelo codigo rapidamente
- saber quais arquivos dependem de quais modulos
- manter ou extender o projeto com seguranca

## Estrutura do projeto

Principais diretorios e arquivos:

```text
.
├── examples/
├── out/
├── src/
│   └── rua/
│       ├── __init__.py
│       ├── tokens.py
│       ├── scanner.py
│       ├── ast_nodes.py
│       ├── parser.py
│       ├── ast_printer.py
│       └── c_transpiler.py
├── tests/
├── demo.py
├── pyproject.toml
└── uv.lock
```

## Para que serve cada area

`examples/`
- Arquivos de exemplo em Rua.
- Uteis para demonstracao, depuracao e validacao ponta a ponta.

`out/`
- Arquivos gerados.
- Normalmente contem arquivos `.ast.txt` e `.c` produzidos pelo `demo.py`.

`src/rua/`
- Implementacao do compilador.
- Este e o principal lugar que um desenvolvedor deve ler primeiro.

`tests/`
- Testes unitarios e testes de smoke para scanner, parser, AST, transpiler e pipeline de demo.

[demo.py](/Users/marceufilho/ibmec/compiladores-marceu/demo.py)
- Ponto de entrada em linha de comando para rodar o pipeline em um arquivo `.rua`.

[pyproject.toml](/Users/marceufilho/ibmec/compiladores-marceu/pyproject.toml)
- Configuracao do projeto.
- Define versao de Python, Ruff e pytest.

## Pipeline atual do compilador

Hoje o compilador funciona assim:

```text
codigo Rua
-> scanner
-> lista de tokens
-> parser
-> AST
-> impressao da AST
-> transpiler para C
```

Isso significa que o projeto atual e:
- um analisador lexico
- um analisador sintatico
- um construtor de AST
- um impressor de AST
- um transpiler simples de AST para C

Ele ainda nao e um compilador completo porque nao existe fase de analise semantica.

## Modulos centrais

### [tokens.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/tokens.py)

Responsabilidade principal:
- definir os tipos de token e a classificacao de palavras-chave

Conteudos importantes:
- `TokenType`: enum com todos os tipos de token
- `Token`: dataclass dos tokens produzidos pelo scanner
- `KEYWORDS`: mapa de palavras reservadas

Dependencias:
- apenas biblioteca padrao

Usado por:
- [scanner.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/scanner.py)
- [parser.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/parser.py)
- testes

Como funciona:
- `TokenType` e o vocabulario compartilhado entre scanner e parser.
- `KEYWORDS` permite ao scanner distinguir identificadores como `main` de palavras-chave como `function`.

### [scanner.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/scanner.py)

Responsabilidade principal:
- converter o texto-fonte em uma lista de tokens

Dependencias:
- `re`
- [tokens.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/tokens.py)

Usado por:
- [parser.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/parser.py)
- [demo.py](/Users/marceufilho/ibmec/compiladores-marceu/demo.py)
- testes

Como funciona:
- constroi uma unica regex combinada com grupos nomeados
- percorre o codigo da esquerda para a direita
- ignora espacos, quebras de linha e comentarios
- produz objetos `Token` com linha e coluna
- reclassifica identificadores em palavras-chave usando `KEYWORDS`

Observacao importante:
- a ordem dos padroes importa, principalmente para operadores como `==` antes de `=`

### [ast_nodes.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/ast_nodes.py)

Responsabilidade principal:
- definir a estrutura da AST

Dependencias:
- `dataclasses`

Usado por:
- [parser.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/parser.py)
- [ast_printer.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/ast_printer.py)
- [c_transpiler.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/c_transpiler.py)
- testes

Como funciona:
- cada construcao da linguagem e representada por uma dataclass
- `Program` e o no raiz
- declaracoes, statements e expressoes sao separados em tipos explicitos

Observacao importante:
- a AST e a representacao central do compilador
- qualquer trabalho futuro de analise semantica ou novos backends deve partir desses nos

### [parser.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/parser.py)

Responsabilidade principal:
- transformar a lista de tokens em AST

Dependencias:
- [tokens.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/tokens.py)
- [ast_nodes.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/ast_nodes.py)

Usado por:
- [demo.py](/Users/marceufilho/ibmec/compiladores-marceu/demo.py)
- testes
- indiretamente por `ast_printer` e `c_transpiler`, por meio da AST gerada

Como funciona:
- parser recursive-descent
- impõe a estrutura de topo: imports, globais e funcoes
- analisa statements e expressoes com niveis explicitos de precedencia
- gera `ParseError` em caso de sintaxe invalida

Observacao importante:
- o parser valida apenas sintaxe
- ele nao valida semantica como variaveis nao declaradas, contagem de argumentos ou consistencia de tipos

### [ast_printer.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/ast_printer.py)

Responsabilidade principal:
- renderizar a AST como uma arvore legivel

Dependencias:
- `pathlib`
- [ast_nodes.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/ast_nodes.py)

Usado por:
- [demo.py](/Users/marceufilho/ibmec/compiladores-marceu/demo.py)
- testes

Como funciona:
- percorre a AST recursivamente
- produz uma arvore textual estavel
- escreve arquivos `.ast.txt`

Observacao importante:
- e util para depurar o parser e para documentar a estrutura da linguagem

### [c_transpiler.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/c_transpiler.py)

Responsabilidade principal:
- gerar codigo C simples a partir da AST

Dependencias:
- `pathlib`
- [ast_nodes.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/ast_nodes.py)

Usado por:
- [demo.py](/Users/marceufilho/ibmec/compiladores-marceu/demo.py)
- testes

Como funciona:
- percorre a AST
- infere tipos C simples para literais e algumas expressoes
- gera globais, funcoes, statements e expressoes em C
- mapeia built-ins da Rua para nomes auxiliares em C

Observacao importante:
- o transpiler usa heuristicas
- por exemplo, os parametros de funcao hoje sao assumidos como `int`
- isso e aceitavel na fase atual do projeto, mas a proxima etapa necessaria e a analise semantica

### [demo.py](/Users/marceufilho/ibmec/compiladores-marceu/demo.py)

Responsabilidade principal:
- executar o pipeline completo a partir de um arquivo-fonte

Dependencias:
- biblioteca padrao: `argparse`, `sys`, `pathlib`
- [scanner.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/scanner.py)
- [parser.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/parser.py)
- [ast_printer.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/ast_printer.py)
- [c_transpiler.py](/Users/marceufilho/ibmec/compiladores-marceu/src/rua/c_transpiler.py)

Como funciona:
- le um arquivo `.rua`
- gera tokens
- gera a AST
- escreve `.ast.txt`
- escreve `.c`

## Resumo das dependencias

Direcao geral das dependencias:

```text
tokens
  -> scanner
  -> parser

ast_nodes
  -> parser
  -> ast_printer
  -> c_transpiler

scanner + parser + ast_printer + c_transpiler
  -> demo
```

Esse fluxo de dependencias e limpo e majoritariamente unidirecional.

## O que o compilador nao faz hoje

A principal fase ausente e a analise semantica.

Isso significa que o compilador atualmente nao verifica completamente:
- variaveis nao declaradas
- declaracoes duplicadas
- quantidade de argumentos em chamadas
- consistencia de tipos
- consistencia de tipos de retorno

Essa e a principal area de trabalho futuro.

## Nota final

O projeto atual foi mantido pequeno e legivel de forma proposital.

Sua maior forca e a clareza:
- o scanner e direto
- o parser e explicito
- os nos da AST sao simples
- as saidas geradas sao faceis de inspecionar

Isso torna o projeto uma boa base para colaboracao, manutencao e futuras fases do compilador.
