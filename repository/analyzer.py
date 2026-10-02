from repository.models import (
    FileInfo,
    RepositoryInfo,
    RepositoryStats,
    RepositorySummary,
)

class RepositoryAnalyzer:
    def __init__(self,repository_info:RepositoryInfo, files:list[FileInfo])->None:
        self.repository_info=repository_info
        self.files=files
    
    def analyze(self)-> RepositorySummary:
        stats=RepositoryStats(
            total_files=len(self.files),
            total_directories=self._count_directories(),
            total_size=self._calculate_size()
        )

        architecture_report = None
        if any(file.extension == ".py" for file in self.files):
            try:
                from code_intelligence.repository_parser import RepositoryParser
                from code_intelligence.analysis.knowledge_graph_builder import KnowledgeGraphBuilder
                from code_intelligence.analysis.dependency_analyzer import DependencyAnalyzer
                from code_intelligence.analysis.graph_index import GraphIndex
                from code_intelligence.analysis.architecture_analyzer import ArchitectureAnalyzer

                # 1. Parse repository python code into code model
                parser = RepositoryParser()
                repo_code_model = parser.parse(self.files)

                # 2. Build the initial knowledge graph nodes/edges
                kg_builder = KnowledgeGraphBuilder()
                graph = kg_builder.build(repo_code_model)

                # 3. Analyze dependencies to add module import edges to the graph
                graph_index = GraphIndex(graph)
                dep_analyzer = DependencyAnalyzer(graph_index)
                graph = dep_analyzer.analyze(repo_code_model, graph)

                # 4. Rebuild graph index containing updated dependency edges
                graph_index = GraphIndex(graph)

                # 5. Run the architecture analyzer using the graph index
                arch_analyzer = ArchitectureAnalyzer(graph_index)
                architecture_report = arch_analyzer.analyze()
            except Exception:
                pass

        return RepositorySummary(
            info= self.repository_info,
            stats=stats,
            files=self.files,
            architecture=architecture_report
        )
    
    def _calculate_size(self)-> int:
        return sum(file.size for file in self.files)

    def _count_directories(self)-> int:
        directories={file.parent for file in self.files}
        return len(directories)
