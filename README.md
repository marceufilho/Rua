# Rua V1 Compiler Prototype

Este projeto implementa um protótipo simples da linguagem Rua V1 em Python.

O pipeline atual faz:

1. leitura do arquivo `.rua`
2. scanner / lexer
3. parser
4. geração da AST em texto
5. transpiração para C

## Requisitos

- Python 3.11+
- `uv`

## Instalação

Na raiz do projeto:

```bash
uv sync
```

## Como executar

Use o script `demo.py` passando um arquivo `.rua`:

```bash
uv run python demo.py examples/minimal.rua
```

Isso gera, por padrão, os arquivos na pasta `out/`:

- `minimal.ast.txt`
- `minimal.c`

Você também pode escolher outra pasta de saída:

```bash
uv run python demo.py examples/pet.rua --out-dir out
```

## Exemplos disponíveis

Os exemplos ficam na pasta `examples/`.

### Exemplo mínimo

```bash
uv run python demo.py examples/minimal.rua
```

### Exemplo do pet

```bash
uv run python demo.py examples/pet.rua
```

### Exemplo de calculadora

```bash
uv run python demo.py examples/calculator.rua
```


## O que sai como resultado

Para cada arquivo de entrada, o projeto gera:

- um arquivo `.ast.txt` com a árvore sintática em formato legível
- um arquivo `.c` com o código C gerado

Exemplo:

```bash
uv run python demo.py examples/calculator.rua --out-dir out
```

Arquivos gerados:

- `out/calculator.ast.txt`
- `out/calculator.c`

## Testes e qualidade

Para rodar os testes:

```bash
uv run pytest -q
```

Para rodar formatação e lint:

```bash
uv run ruff format .
uv run ruff check .
```

## Documentação

- [RUA_QUICKSTART.md](/Users/marceufilho/ibmec/compiladores-marceu/RUA_QUICKSTART.md): guia rápido da linguagem para novos usuários
- [Documento Tecnico](/Users/marceufilho/ibmec/compiladores-marceu/Documento-tecnico-RUA.md): documento técnico explicando como o compilador funciona hoje
- [Visao do codigo](/Users/marceufilho/ibmec/compiladores-marceu/Overview-Codigo.md): visão geral do código para manutenção e colaboração

## Observações

- A linguagem ainda é pequena e propositalmente simples.
- `print(...)`, `println(...)` e `read_line()` foram modeladas como built-ins.
- O exemplo `tic_tac_toe.rua` é pensado para o estilo embarcado da linguagem, não para terminal tradicional.
