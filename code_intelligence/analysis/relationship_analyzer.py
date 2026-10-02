from code_intelligence.models import (
    RepositoryCodeModel,
    ModuleInfo,
    ClassInfo,
)

from code_intelligence.analysis.relationship_models import (
    RepositoryRelationshipModel,
    RelationshipInfo,
    RelationshipKind,
)


class RelationshipAnalyzer:
    """
    Builds relationships between symbols in the repository.
    """

    def analyze(
        self,
        repository: RepositoryCodeModel,
    ) -> RepositoryRelationshipModel:
        """
        Analyze the repository and build the relationship model.
        """

        relationships = RepositoryRelationshipModel()

        for module in repository.modules:
            self._analyze_module(
                relationships,
                module,
            )

        return relationships

    def _analyze_module(
        self,
        relationships: RepositoryRelationshipModel,
        module: ModuleInfo,
    ) -> None:
        """
        Analyze one module.
        """

        for cls in module.classes:
            self._analyze_class(
                relationships,
                cls,
            )

    def _analyze_class(
        self,
        relationships: RepositoryRelationshipModel,
        cls: ClassInfo,
    ) -> None:
        """
        Analyze one class.
        """

        for method in cls.methods:
            relationships.relationships.append(
                RelationshipInfo(
                    source=cls.qualified_name,
                    target=method.qualified_name,
                    kind=RelationshipKind.OWNS,
                )
            )

        for base_class in cls.base_classes:
            relationships.relationships.append(
                RelationshipInfo(
                    source=cls.qualified_name,
                    target=base_class,
                    kind=RelationshipKind.INHERITS,
                )
            )