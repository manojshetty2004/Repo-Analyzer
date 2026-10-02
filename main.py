from repository import detector
from ui.display import display_summary
from repository.loader import RepositoryLoader
from repository.scanner import RepositoryScanner
from repository.analyzer import RepositoryAnalyzer
from repository.models import RepositoryInfo
from repository.detector import RepositoryDetector
def main():
#C:\Users\yasha\OneDrive\Documents\Plant prediction
    repo_path=input ("Enter the path to the repository: ")
    loader=RepositoryLoader(repo_path)
    scanner=RepositoryScanner(loader.get_root_path())
    files=scanner.scan()
    print(len(files))
    
    for file in files:
        print(file.relative_path)
    repository_info=RepositoryInfo(
        name=loader.get_repository_name(),
        root_path=str(loader.get_root_path()),
        languages=[],
        framework=None,
        database=None,
        entry_point=None
    )
    detector = RepositoryDetector(repository_info, files)
    repository_info = detector.detect()
    analyzer=RepositoryAnalyzer(repository_info,files)
    summary=analyzer.analyze()

    display_summary(summary)


   
if __name__ == "__main__":
    main()
