from code_intelligence.chunking.models import CodeChunk
from code_intelligence.models import RepositoryCodeModel

from code_intelligence.analysis.graph_index import GraphIndex

from code_intelligence.analysis.knowledge_graph_builder import (
    KnowledgeGraphBuilder,
)

from code_intelligence.analysis.dependency_analyzer import (
    DependencyAnalyzer,
)

from code_intelligence.analysis.call_graph_builder import (
    CallGraphBuilder,
)

from code_intelligence.analysis.repository_statistics import (
    RepositoryStatisticsAnalyzer,
)

from code_intelligence.analysis.architecture_analyzer import (
    ArchitectureAnalyzer,
)

from code_intelligence.analysis.coupling_analyzer import (
    CouplingAnalyzer,
)

from code_intelligence.analysis.complexity_analyzer import (
    ComplexityAnalyzer,
)

from code_intelligence.analysis.dead_code_detector import (
    DeadCodeDetector,
)

from code_intelligence.analysis.circular_dependency_detector import (
    CircularDependencyDetector,
)

from code_intelligence.analysis.duplicate_code_detector import (
    DuplicateCodeDetector,
)

from code_intelligence.analysis.repository_analysis_models import (
    RepositoryAnalysisReport,
)


class RepositoryAnalysisService:
    """
    Runs every repository analyzer and combines the results.
    """

    def __init__(self) -> None:
        self.graph_builder = KnowledgeGraphBuilder()
        self.call_graph_builder = CallGraphBuilder()
        self.duplicate_detector = DuplicateCodeDetector()
        self._last_report = None
    def analyze(
        self,
        repository: RepositoryCodeModel,
        chunks: list[CodeChunk],
    ) -> RepositoryAnalysisReport:
        """
        Run every repository analysis.
        """

        #
        # Build graph
        #

        graph = self.graph_builder.build(repository)

        #
        # Initial graph index
        #

        index = GraphIndex(graph)

        #
        # Add dependency edges
        #

        dependency_analyzer = DependencyAnalyzer(index)

        graph = dependency_analyzer.analyze(
            repository,
            graph,
        )

        #
        # Add call edges
        #

        graph = self.call_graph_builder.build(
            repository,
            graph,
        )

        #
        # Rebuild index because new edges were added
        #

        index = GraphIndex(graph)

        #
        # Run analyzers
        #

        statistics = RepositoryStatisticsAnalyzer(
            index,
        ).analyze()

        architecture = ArchitectureAnalyzer(
            index,
        ).analyze()

        coupling = CouplingAnalyzer(
            index,
        ).analyze()

        complexity = ComplexityAnalyzer(
            index,
        ).analyze()

        dead_code = DeadCodeDetector(
            index,
        ).analyze()

        circular_dependencies = CircularDependencyDetector(
            index,
        ).analyze()

        duplicate_code = self.duplicate_detector.analyze(
            chunks,
        )

        report = RepositoryAnalysisReport(
            statistics=statistics,
            architecture=architecture,
            coupling=coupling,
            complexity=complexity,
            dead_code=dead_code,
            circular_dependencies=circular_dependencies,
            duplicate_code=duplicate_code,
        )
        self._last_report = report
        return report

    def last_report(self) -> RepositoryAnalysisReport:
    

        if self._last_report is None:
            raise RuntimeError(
                "Repository has not been analyzed yet."
            )

        return self._last_report
