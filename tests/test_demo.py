from pathlib import Path

import pytest

from demo import main, run_pipeline


def test_demo_pipeline_on_minimal_example(tmp_path: Path) -> None:
    ast_path, c_path = run_pipeline("examples/minimal.rua", tmp_path)

    assert ast_path == tmp_path / "minimal.ast.txt"
    assert c_path == tmp_path / "minimal.c"
    assert ast_path.exists()
    assert c_path.exists()
    assert "Program" in ast_path.read_text(encoding="utf-8")
    assert "void main(void)" in c_path.read_text(encoding="utf-8")


def test_demo_cli_writes_output_files_and_returns_zero(tmp_path: Path, capsys) -> None:
    exit_code = main(["examples/minimal.rua", "--out-dir", str(tmp_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Wrote AST to" in captured.out
    assert "Wrote C to" in captured.out
    assert (tmp_path / "minimal.ast.txt").exists()
    assert (tmp_path / "minimal.c").exists()


@pytest.mark.parametrize(
    "example_name",
    [
        "minimal.rua",
        "pet.rua",
        "calculator.rua",
        "console_io.rua",
    ],
)
def test_all_main_examples_run_end_to_end(example_name: str, tmp_path: Path) -> None:
    ast_path, c_path = run_pipeline(Path("examples") / example_name, tmp_path)

    assert ast_path.exists()
    assert c_path.exists()
    assert ast_path.read_text(encoding="utf-8").startswith("Program")
    assert "#include <stdbool.h>" in c_path.read_text(encoding="utf-8")
