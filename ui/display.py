from rich.console import Console
from  rich.table import Table
from repository.models import RepositorySummary

console=Console()

def display_summary(summary:RepositorySummary)->None:
    table = Table(title="Repository Summary")

    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("Repository", summary.info.name)
    table.add_row("Root Path", summary.info.root_path)
    table.add_row("Languages", ", ".join(summary.info.languages) or "Unknown")
    table.add_row("Framework", summary.info.framework or "Unknown")
    table.add_row("Database", summary.info.database or "Unknown")
    table.add_row("Entry Point", summary.info.entry_point or "Unknown")
    table.add_row("Total Files", str(summary.stats.total_files))
    table.add_row("Total Directories", str(summary.stats.total_directories))
    table.add_row(
        "Total Size",
        f"{summary.stats.total_size:,} bytes",
    )

    console.print(table)

    if summary.architecture:
        arch = summary.architecture
        arch_table = Table(title="Code Architecture & Dependency Report")

        arch_table.add_column("Aspect", style="cyan", no_wrap=True)
        arch_table.add_column("Details", style="green")

        arch_table.add_row("Total Python Modules", str(len(arch.modules)))
        arch_table.add_row("Entry Points (No Imports)", ", ".join(arch.entry_points) or "None")
        arch_table.add_row("Leaf Modules (Imports Nothing)", ", ".join(arch.leaf_modules) or "None")

        # Format top 5 most connected modules
        conn_str = ", ".join(f"{mc.module} ({mc.connections} connections)" for mc in arch.most_connected[:5])
        arch_table.add_row("Most Connected Modules", conn_str or "None")

        # Sample import mappings
        dep_lines = []
        for src, targets in list(arch.dependencies.items())[:5]:
            dep_lines.append(f"{src} imports: {', '.join(targets)}")
        if len(arch.dependencies) > 5:
            dep_lines.append(f"... and {len(arch.dependencies) - 5} more")
        arch_table.add_row("Import Mappings (Sample)", "\n".join(dep_lines) or "None")

        console.print()
        console.print(arch_table)