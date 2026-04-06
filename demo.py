"""Demo CLI for the Rua V1 compiler pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rua.ast_printer import write_ast
from rua.c_transpiler import write_c
from rua.parser import ParseError, Parser
from rua.scanner import ScanError, Scanner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Rua V1 scanner, parser, AST printer, and C transpiler.")
    parser.add_argument("input", help="Path to the input .rua file")
    parser.add_argument(
        "--out-dir",
        default="out",
        help="Directory where the generated .ast.txt and .c files will be written",
    )
    return parser


def run_pipeline(input_path: str | Path, out_dir: str | Path = "out") -> tuple[Path, Path]:
    source_path = Path(input_path)
    output_dir = Path(out_dir)

    source = source_path.read_text(encoding="utf-8")
    tokens = Scanner(source).scan_tokens()
    program = Parser(tokens).parse()

    output_dir.mkdir(parents=True, exist_ok=True)

    stem = source_path.stem
    ast_path = output_dir / f"{stem}.ast.txt"
    c_path = output_dir / f"{stem}.c"

    write_ast(program, ast_path)
    write_c(program, c_path)

    return ast_path, c_path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        ast_path, c_path = run_pipeline(args.input, args.out_dir)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except (ScanError, ParseError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote AST to {ast_path}")
    print(f"Wrote C to {c_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
