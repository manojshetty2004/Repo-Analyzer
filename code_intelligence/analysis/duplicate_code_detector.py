import hashlib

from collections import defaultdict

from code_intelligence.chunking.models import CodeChunk
from code_intelligence.analysis.models import (
    DuplicateCodeGroup,
    DuplicateCodeReport,
)


class DuplicateCodeDetector:
    """
    Detect duplicate code chunks.
    """

    def analyze(
        self,
        chunks: list[CodeChunk],
    ) -> DuplicateCodeReport:

        hashes = defaultdict(list)

        for chunk in chunks:

            normalized = self._normalize(
                chunk.content,
            )

            digest = hashlib.sha256(
                normalized.encode()
            ).hexdigest()

            hashes[digest].append(chunk.id)

        duplicates = []

        for digest, ids in hashes.items():

            if len(ids) < 2:
                continue

            duplicates.append(
                DuplicateCodeGroup(
                    hash=digest,
                    chunks=ids,
                )
            )

        return DuplicateCodeReport(
            duplicates=duplicates,
        )

    def _normalize(
        self,
        code: str,
    ) -> str:
        """
        Normalize source code before hashing.
        """

        lines = []

        for line in code.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            lines.append(line)

        return "\n".join(lines)