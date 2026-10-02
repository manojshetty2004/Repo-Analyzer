from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from git import Repo


def normalize_url(path_str: str) -> str:
    path_str = path_str.strip()
    lower_str = path_str.lower()
    if lower_str.startswith("http:") or lower_str.startswith("https:"):
        prefix, rest = path_str.split(":", 1)
        rest = rest.replace("\\\\", "/").replace("\\", "/")
        parts = [p for p in rest.split("/") if p]
        if parts:
            rest = "//" + "/".join(parts)
        return f"{prefix}:{rest}"
    return path_str


class GitHubRepository:
    """
    Clones a GitHub repository into a temporary directory.

    Usage:
        github_repo = GitHubRepository(url)
        local_path = github_repo.clone()

        try:
            indexer.index(local_path)
        finally:
            github_repo.cleanup()
    """

    def __init__(self, repository_url: str):
        self.repository_url = normalize_url(repository_url)

        if not self._is_valid_github_url():
            raise ValueError("Invalid GitHub repository URL.")

        self._temp_directory: Path | None = None
        self._repository_path: Path | None = None

    def clone(self) -> Path:
        """
        Clone the GitHub repository into a temporary directory.
        Returns the local repository path.
        """

        self._temp_directory = Path(tempfile.mkdtemp(prefix="aise_repo_"))

        repository_name = (
            Path(urlparse(self.repository_url).path).stem
            or "repository"
        )

        self._repository_path = self._temp_directory / repository_name

        Repo.clone_from(
            self.repository_url,
            self._repository_path,
            depth=1,      # Shallow clone (faster)
        )

        return self._repository_path

    def cleanup(self) -> None:
        """Delete the cloned repository."""

        if (
            self._temp_directory is not None
            and self._temp_directory.exists()
        ):
            shutil.rmtree(self._temp_directory, ignore_errors=True)

    def _is_valid_github_url(self) -> bool:
        parsed = urlparse(self.repository_url)

        if parsed.scheme not in ("http", "https"):
            return False

        if parsed.netloc.lower() != "github.com":
            return False

        parts = [
            part
            for part in parsed.path.split("/")
            if part
        ]

        return len(parts) >= 2