from pydantic import BaseModel, Field
from code_intelligence.analysis.models import ArchitectureReport
class FileInfo(BaseModel):
    name: str = Field(..., description="The name of the file")
    path: str = Field(..., description="Absolute path of the file in the local file system.")
    relative_path: str = Field(...,description="Path of the file relative to the repository root.")
    extension: str = Field(...,description="File extension such as .py, .js, .java, or .md.")
    size: int = Field(...,description="Size of the file in bytes.")
    parent: str = Field(...,description="Parent directory containing the file.")

class RepositoryStats(BaseModel):
    total_files: int=Field(...,description="Total number of files in the repository.")
    total_directories: int=Field(...,description="Total number of directories in the repository.")
    total_size: int =Field(...,description="Total size of the all repository files in bytes.")

class RepositoryInfo(BaseModel):
    name:str=Field(...,description="Name of the repository.")
    root_path:str=Field(...,descriptiion="Absolute path of the repository root directory.")
    languages: list[str]=Field(default_factory=list,description="List of programming languages used in the repository.")
    framework: str | None = Field(None,description="Framework ddetectedd in the repository, such as Django, Flask, React, Angular, etc.")
    database:str | None = Field(None,description="Database Technology used by the project, such as MySQL, PostgreSQL, MongoDB, etc.")
    entry_point:str | None =Field(None,description=" Main entry point of the project, such as main.py, index.js, app.py,etc.")


    
    

class RepositorySummary(BaseModel):
    info : RepositoryInfo = Field(...,description="general metadata about the repository")
    stats: RepositoryStats= Field(...,description="statistical information about the repository")
    files: list[FileInfo]= Field(...,description="List contaniing metadata for every discovered file.")
    architecture: ArchitectureReport | None = Field(None, description="Code intelligence architecture report of the repository")
