from pathlib import Path

from code_intelligence.repository_parser import RepositoryParser
from code_intelligence.chunking.chunker import Chunker
from code_intelligence.indexing.repository_indexer import RepositoryIndexer
from code_intelligence.rag.rag_engine import RagEngine
from code_intelligence.analysis.repository_analysis_service import (
    RepositoryAnalysisService,
)
from code_intelligence.cli.formatter import ReportFormatter

class CLICommands:
    """
    Implements all CLI commands.
    """

    def __init__(
        self,
        parser: RepositoryParser,
        chunker: Chunker,
        indexer: RepositoryIndexer,
        rag: RagEngine,
        analysis: RepositoryAnalysisService,
    ) -> None:

        self._parser = parser
        self._chunker = chunker
        self._indexer = indexer
        self._rag = rag
        self._analysis = analysis

    def index(
        self,
        repository: str,
    ) -> None:

        repository_model = self._parser.parse(
            repository,
        )

        chunks = self._chunker.build_chunks(
            repository_model,
        )

        self._indexer.index_model(
            repository_model,
            chunks,
        )

        self._analysis.analyze(
            repository_model,
            chunks,
        )

        print("Repository indexed successfully.")

    def ask(
        self,
        question: str,
    ) -> str:

        answer = self._rag.answer(question)

        print(answer)
        return answer

    def statistics(self, repository: str):

        report = self.analyze(repository)

        print(
            ReportFormatter.statistics(report)
        )

    def architecture(self, repository: str):

        report = self.analyze(repository)

        print(
            ReportFormatter.architecture(report)
        )

    def complexity(self, repository: str):

        report = self.analyze(repository)

        print(
            ReportFormatter.complexity(report)
        )

    def coupling(self, repository: str):

        report = self.analyze(repository)

        print(
            ReportFormatter.coupling(report)
        )

    def dead_code(self, repository: str):

        report = self.analyze(repository)

        print(
            ReportFormatter.dead_code(report)
        )

    def duplicates(self, repository: str):

        report = self.analyze(repository)

        print(
            ReportFormatter.duplicates(report)
        )

    def circular(self, repository: str):

        report = self.analyze(repository)

        print(
            ReportFormatter.circular(report)
        )

    def analyze(
        self,
        repository: str,
    ):

        repository_model = self._parser.parse(
            repository,
        )

        chunks = self._chunker.build_chunks(
            repository_model,
        )

        report = self._analysis.analyze(
            repository_model,
            chunks,
        )

        return report