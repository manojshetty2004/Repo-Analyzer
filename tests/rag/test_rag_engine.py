from unittest.mock import Mock, patch
from code_intelligence.rag.rag_engine import RagEngine
from code_intelligence.routing.intent import Intent


def test_rag_engine_rag_flow():
    llm = Mock()
    search = Mock()
    context = Mock()
    graph_context = Mock()
    prompt_builder = Mock()
    router = Mock()
    analysis = Mock()
    memory = Mock()

    # Configure mock returns
    router.route.return_value = Intent.RAG
    search.search.return_value = ["mock_result"]
    context.build.return_value = "repository_context"
    graph_context.build.return_value = "graph_context"
    memory.build_context.return_value = "conversation_context"
    prompt_builder.build.return_value = "built_prompt"
    llm.generate.return_value = "generated_answer"

    engine = RagEngine(
        llm_provider=llm,
        search_service=search,
        context_builder=context,
        graph_context_builder=graph_context,
        prompt_builder=prompt_builder,
        router=router,
        analysis=analysis,
        memory=memory,
    )

    answer = engine.answer("How does X work?")
    assert answer == "generated_answer"

    router.route.assert_called_once_with("How does X work?")
    search.search.assert_called_once_with("How does X work?")
    context.build.assert_called_once()
    graph_context.build.assert_called_once()
    prompt_builder.build.assert_called_once_with(
        question="How does X work?",
        repository_context="repository_context",
        graph_context="graph_context",
        conversation_context="conversation_context",
    )
    llm.generate.assert_called_once_with("built_prompt")
    memory.add.assert_called_once_with("How does X work?", "generated_answer")


@patch("code_intelligence.rag.rag_engine.ReportFormatter")
def test_rag_engine_routed_intent(mock_formatter):
    llm = Mock()
    search = Mock()
    context = Mock()
    graph_context = Mock()
    prompt_builder = Mock()
    router = Mock()
    analysis = Mock()
    memory = Mock()

    router.route.return_value = Intent.STATISTICS
    report = Mock()
    analysis.last_report.return_value = report
    mock_formatter.statistics.return_value = "mock_stats_output"

    engine = RagEngine(
        llm_provider=llm,
        search_service=search,
        context_builder=context,
        graph_context_builder=graph_context,
        prompt_builder=prompt_builder,
        router=router,
        analysis=analysis,
        memory=memory,
    )

    answer = engine.answer("Show me stats")
    assert answer == "mock_stats_output"
    analysis.last_report.assert_called_once()
    mock_formatter.statistics.assert_called_once_with(report)
