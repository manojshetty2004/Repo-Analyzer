from code_intelligence.analysis.repository_analysis_models import (
    RepositoryAnalysisReport,
)


class ReportFormatter:
    """
    Formats analysis reports for CLI output.
    """

    @staticmethod
    def statistics(report: RepositoryAnalysisReport) -> str:

        stats = report.statistics

        return f"""
Repository Statistics
=====================

Modules   : {stats.total_modules}
Classes   : {stats.total_classes}
Functions : {stats.total_functions}
Methods   : {stats.total_methods}
Imports   : {stats.total_imports}

Graph Nodes : {stats.total_graph_nodes}
Graph Edges : {stats.total_graph_edges}
""".strip()

    @staticmethod
    def architecture(report: RepositoryAnalysisReport) -> str:

        architecture = report.architecture

        lines = [
            "Architecture",
            "============",
            "",
            "Entry Points",
            "------------",
        ]

        for module in architecture.entry_points:
            lines.append(module)

        lines.extend(
            [
                "",
                "Leaf Modules",
                "------------",
            ]
        )

        for module in architecture.leaf_modules:
            lines.append(module)

        lines.extend(
            [
                "",
                "Most Connected Modules",
                "----------------------",
            ]
        )

        for conn in architecture.most_connected:
            lines.append(f"  {conn.module} ({conn.connections} connections)")

        return "\n".join(lines)

    @staticmethod
    def complexity(report: RepositoryAnalysisReport) -> str:

        complexity = report.complexity

        lines = [
            "Repository Complexity",
            "=====================",
            "",
        ]

        if not complexity.modules:
            lines.append("No modules found to analyze complexity.")
            return "\n".join(lines)

        total_score = sum(m.complexity_score for m in complexity.modules)
        avg_score = total_score / len(complexity.modules)
        lines.append(f"Average Complexity Score: {avg_score:.2f}")
        lines.append(f"Total Complexity Score:   {total_score}")
        lines.append("")
        lines.append("Complexity by Module:")
        lines.append("---------------------")

        for m in complexity.modules[:10]:
            lines.append(f"  {m.module}: {m.complexity_score}")

        if len(complexity.modules) > 10:
            lines.append(f"  ... and {len(complexity.modules) - 10} more modules.")

        return "\n".join(lines)

    @staticmethod
    def coupling(report: RepositoryAnalysisReport) -> str:

        lines = [
            "Module Coupling",
            "================",
            "",
        ]

        for module in report.coupling.modules:

            lines.extend(
                [
                    module.module,
                    f"  Incoming : {module.incoming_dependencies}",
                    f"  Outgoing : {module.outgoing_dependencies}",
                    f"  Total    : {module.total_dependencies}",
                    "",
                ]
            )

        return "\n".join(lines)

    @staticmethod
    def dead_code(report: RepositoryAnalysisReport) -> str:

        dead = report.dead_code

        lines = [
            "Dead Code",
            "=========",
            "",
            "Unused Modules",
            "--------------",
        ]

        lines.extend(dead.unused_modules)

        lines.extend(
            [
                "",
                "Unused Classes",
                "--------------",
            ]
        )

        lines.extend(dead.unused_classes)

        lines.extend(
            [
                "",
                "Unused Functions",
                "----------------",
            ]
        )

        lines.extend(dead.unused_functions)

        return "\n".join(lines)

    @staticmethod
    def circular(report: RepositoryAnalysisReport) -> str:

        lines = [
            "Circular Dependencies",
            "=====================",
            "",
        ]

        if not report.circular_dependencies.cycles:
            lines.append("No circular dependencies found.")
            return "\n".join(lines)

        for cycle in report.circular_dependencies.cycles:

            lines.append(
                " -> ".join(cycle)
            )

        return "\n".join(lines)

    @staticmethod
    def duplicates(report: RepositoryAnalysisReport) -> str:

        lines = [
            "Duplicate Code",
            "==============",
            "",
        ]

        if not report.duplicate_code.duplicates:
            lines.append("No duplicate code found.")
            return "\n".join(lines)

        for duplicate in report.duplicate_code.duplicates:

            lines.append(f"Hash : {duplicate.hash}")

            for chunk in duplicate.chunks:
                lines.append(f"  {chunk}")

            lines.append("")

        return "\n".join(lines)