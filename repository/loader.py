from pathlib import Path


class RepositoryLoader:
    def __init__(self, root_path: str):
        self.raw_path = root_path.strip()
        self.github_repo = None
        self.repository_path = None

    def _is_github_url(self, url: str) -> bool:
        try:
            from code_intelligence.utils.github import normalize_url
            normalized = normalize_url(url)
            from urllib.parse import urlparse
            parsed = urlparse(normalized)
            if parsed.scheme not in ("http", "https"):
                return False
            if parsed.netloc.lower() != "github.com":
                return False
            parts = [p for p in parsed.path.split("/") if p]
            return len(parts) >= 2
        except Exception:
            return False

    def validate(self) -> bool:
        if self._is_github_url(self.raw_path):
            if not self.repository_path:
                from code_intelligence.utils.github import GitHubRepository
                try:
                    self.github_repo = GitHubRepository(self.raw_path)
                    self.repository_path = self.github_repo.clone()
                except Exception as e:
                    self.cleanup()
                    raise ValueError(f"Failed to clone repository: {e}") from e
            return True
        else:
            self.repository_path = Path(self.raw_path)
            if not self.repository_path.exists():
                raise FileNotFoundError(f"Repository path '{self.repository_path}' does not exist.")
            if not self.repository_path.is_dir():
                raise NotADirectoryError(f"Repository path '{self.repository_path}' is not a directory.")
            return True

    def get_root_path(self) -> Path:
        if self.repository_path is None:
            self.validate()
        return self.repository_path.resolve()

    def get_repository_name(self) -> str:
        if self.repository_path is None:
            self.validate()
        return self.repository_path.resolve().name

    def cleanup(self) -> None:
        if self.github_repo:
            self.github_repo.cleanup()
            self.github_repo = None
            self.repository_path = None