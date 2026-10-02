from pathlib import Path
from code_intelligence.repository_parser import RepositoryParser
from repository.models import FileInfo


def test_repository_parser_with_file_list(tmp_path):
    file1 = tmp_path / "foo.py"
    file1.write_text("def foo(): pass")

    file2 = tmp_path / "bar.py"
    file2.write_text("def bar(): pass")

    # Non-python file
    file3 = tmp_path / "readme.md"
    file3.write_text("hello")

    files = [
        FileInfo(
            name="foo.py",
            path=str(file1),
            relative_path="foo.py",
            extension=".py",
            size=15,
            parent=str(tmp_path),
        ),
        FileInfo(
            name="bar.py",
            path=str(file2),
            relative_path="bar.py",
            extension=".py",
            size=15,
            parent=str(tmp_path),
        ),
        FileInfo(
            name="readme.md",
            path=str(file3),
            relative_path="readme.md",
            extension=".md",
            size=5,
            parent=str(tmp_path),
        ),
    ]

    parser = RepositoryParser()
    repo_model = parser.parse(files)

    assert len(repo_model.modules) == 2
    paths = {Path(m.path).name for m in repo_model.modules}
    assert paths == {"foo.py", "bar.py"}

    foo_module = [m for m in repo_model.modules if Path(m.path).name == "foo.py"][0]
    assert len(foo_module.functions) == 1
    assert foo_module.functions[0].source_code == "def foo(): pass"
