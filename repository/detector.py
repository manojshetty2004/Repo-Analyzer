from pathlib import Path
import os
from repository.models import FileInfo, RepositoryInfo
from repository.constants import LANGUAGE_MAP, FRAMEWORK_PATTERNS, DATABASE_PATTERNS, ENTRY_POINTS, DEPENDENCY_FILES

class RepositoryDetector:
    
    
    def __init__(self,repository_info:RepositoryInfo,files:list[FileInfo])-> None:
        self._repository_info=repository_info
        self._files=files
    
    def detect(self)->RepositoryInfo:
        self._repository_info.languages = self._detect_languages()
        self._repository_info.framework = self._detect_framework()
        self._repository_info.entry_point = self._detect_entry_point()
        self._repository_info.database = self._detect_database()

        return self._repository_info
    
    def _read_file(self, path: Path) -> str:
        """
        Safely read a file and return its lowercase content.
        """

        try:
            return path.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()
        except OSError:
            return ""
    def _find_pattern(self,patterns: dict[str, list[str]],) -> str | None:
        """Search dependency files for known technology patterns."""

        for file in self._files:

            if file.name not in DEPENDENCY_FILES:
                continue

            content = self._read_file(Path(file.path))

            if not content:
                continue

            for technology, keywords in patterns.items():

                if any(
                    keyword.lower() in content
                    for keyword in keywords
                ):
                    return technology

        return None
    def _detect_languages(self)->list[str]:
        languages:set[str]=set()

        for files in self._files:
            language=LANGUAGE_MAP.get(files.extension.lower())
            if language:
                languages.add(language)
        return sorted(languages)
    
    def _detect_framework(self)->str|None:
        return self._find_pattern(FRAMEWORK_PATTERNS)
    
    def _detect_entry_point(self)->str|None:
        file_lookup={
            file.name : file.relative_path
            for file in self._files
        }
        for entry in ENTRY_POINTS:
            if entry in file_lookup:
                return file_lookup[entry]
        return None
    
    def _detect_database(self)->str|None:
        for file in self._files:

            if file.name not in DEPENDENCY_FILES:
                continue

            try:
                content = Path(file.path).read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()
            except Exception:
                continue

            for database, patterns in DATABASE_PATTERNS.items():
                if any(pattern.lower() in content for pattern in patterns):
                    return database

        return None

