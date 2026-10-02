
from pathlib import Path
from repository.models import FileInfo
from repository.constants import IGNORED_DIRECTORIES
import os

class RepositoryScanner:
    def __init__(self, root_path: Path)-> None:
        self.repository_path = root_path
    
    def scan(self)->list[FileInfo]:
        files: list[FileInfo] = []

        for root, dirs, filenames in os.walk(self.repository_path):

            dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORED_DIRECTORIES
            ]

            root_path = Path(root)

            for filename in filenames:

                path = root_path / filename

                try:
                    files.append(self._create_file_info(path))
                except OSError:
                    continue

        return files
   
    
    def _create_file_info(self, path: Path)-> FileInfo:
        return FileInfo(
            name=path.name,
            path=str(path.resolve()),
            relative_path=str(path.relative_to(self.repository_path)),
            extension=path.suffix,
            size=path.stat().st_size,
            parent=str(path.parent.relative_to(self.repository_path)),
        )
    