from pydantic import BaseModel

from code_intelligence.analysis.models import (
    ArchitectureReport,
    RepositoryStatistics,
    CouplingReport,
    ComplexityReport,
    DeadCodeReport,
    CircularDependencyReport,
    DuplicateCodeReport,
)


class RepositoryAnalysisReport(BaseModel):
    """
    Combined report containing every repository analysis.
    """

    statistics: RepositoryStatistics
    architecture: ArchitectureReport
    coupling: CouplingReport
    complexity: ComplexityReport
    dead_code: DeadCodeReport
    circular_dependencies: CircularDependencyReport
    duplicate_code: DuplicateCodeReport