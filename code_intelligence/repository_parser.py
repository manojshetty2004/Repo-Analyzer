from pathlib import Path
from repository.models import FileInfo
from repository.loader import RepositoryLoader
from repository.scanner import RepositoryScanner
from code_intelligence.parser import PythonParser, JSParser
from code_intelligence.models import RepositoryCodeModel


class RepositoryParser:
    def __init__(self) -> None:
        self._python_parser = PythonParser()
        self._js_parser = JSParser()

    def parse(self, files: list[FileInfo] | str | Path) -> RepositoryCodeModel:
        loader = None
        if isinstance(files, (str, Path)):
            loader = RepositoryLoader(str(files))
            try:
                loader.validate()
                scanner = RepositoryScanner(loader.get_root_path())
                files = scanner.scan()
            except Exception as e:
                if loader:
                    loader.cleanup()
                raise e

        try:
            repository = RepositoryCodeModel()
            SUPPORTED_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx"}
            
            for file in files:
                file_path = Path(file.path)
                if file_path.suffix not in SUPPORTED_SUFFIXES:
                    continue
                
                try:
                    if file_path.suffix == ".py":
                        module = self._python_parser.parse(file_path)
                    else:
                        module = self._js_parser.parse(file_path)
                    repository.modules.append(module)
                except Exception:
                    continue

            return repository
        finally:
            if loader:
                loader.cleanup()
