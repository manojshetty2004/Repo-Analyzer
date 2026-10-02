from code_intelligence.cli.commands import CLICommands

from code_intelligence.repository_parser import RepositoryParser
from code_intelligence.chunking.chunker import Chunker

from code_intelligence.indexing.repository_indexer import RepositoryIndexer

from code_intelligence.rag.rag_engine import RagEngine

from code_intelligence.analysis.repository_analysis_service import (
    RepositoryAnalysisService,
)

# New dependencies
from code_intelligence.embeddings.ollama import OllamaEmbeddingProvider
from code_intelligence.vector_store.chroma import ChromaStore
from code_intelligence.llm.ollama import OllamaLLMProvider
from code_intelligence.search.repository_search import RepositorySearchService
from code_intelligence.context.context_builder import ContextBuilder
from code_intelligence.rag.graph_context_builder import GraphContextBuilder
from code_intelligence.rag.prompt_builder import PromptBuilder
from code_intelligence.memory.conversation_memory import ConversationMemory
from code_intelligence.routing.intent_router import IntentRouter



def build_application():

    #
    # Build every dependency here.
    #

    parser = RepositoryParser()

    chunker = Chunker()

    #
    # Embedding provider (using the nomic embedding model found locally)
    #
    embedding_provider = OllamaEmbeddingProvider(model_name="nomic-embed-text-v2-moe:latest")

    #
    # Vector Store backed by ChromaDB
    #
    vector_store = ChromaStore(
        persist_directory=".chromadb",
        collection_name="assistant",
    )

    #
    # LLM Provider (using the llama3.2:3b model found locally)
    #
    llm = OllamaLLMProvider(model="llama3.2:3b")

    indexer = RepositoryIndexer(
        parser,
        chunker,
        embedding_provider,
        vector_store,
    )

    #
    # RAG Engine sub-components
    #
    search_service = RepositorySearchService(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    context_builder = ContextBuilder()
    graph_context_builder = GraphContextBuilder()
    prompt_builder = PromptBuilder()
    memory = ConversationMemory()

    analysis = RepositoryAnalysisService()

    router = IntentRouter()

    #
    # Main RAG coordinator
    #
    rag = RagEngine(
        llm_provider=llm,
        search_service=search_service,
        context_builder=context_builder,
        graph_context_builder=graph_context_builder,
        prompt_builder=prompt_builder,
        router=router,
        analysis=analysis,
        memory=memory,
    )


    return CLICommands(
        parser,
        chunker,
        indexer,
        rag,
        analysis,
    )