"""
Centralized constants used by the repository intelligence layer.

Keeping all detection rules in one place makes the system easier to
maintain and extend.
"""

# -------------------------------------------------
# Scanner
# -------------------------------------------------

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "ENV",
    "Lib",
    "Scripts",
    "Include",
    "bin",
    "obj",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
}


# -------------------------------------------------
# Language Detection
# -------------------------------------------------

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".kt": "Kotlin",
    ".swift": "Swift",
}


# -------------------------------------------------
# Dependency Files
# -------------------------------------------------

DEPENDENCY_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "Pipfile",
    "poetry.lock",
}


# -------------------------------------------------
# Framework Detection
# -------------------------------------------------

FRAMEWORK_PATTERNS = {
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Streamlit": ["streamlit"],
    "React": ["react"],
    "Next.js": ["next"],
    "Express": ["express"],
    "Vue": ["vue"],
    "Angular": ["@angular/core"],
}


# -------------------------------------------------
# Database Detection
# -------------------------------------------------

DATABASE_PATTERNS = {
    "SQLite": ["sqlite3"],
    "PostgreSQL": ["psycopg2", "asyncpg"],
    "MySQL": ["mysqlclient", "pymysql"],
    "MongoDB": ["pymongo", "motor"],
    "SQLAlchemy": ["sqlalchemy"],
}


# -------------------------------------------------
# Entry Point Detection
# -------------------------------------------------

ENTRY_POINTS = (
    "main.py",
    "app.py",
    "run.py",
    "manage.py",
    "index.js",
    "server.js",
    "main.ts",
    "Program.cs",
)



