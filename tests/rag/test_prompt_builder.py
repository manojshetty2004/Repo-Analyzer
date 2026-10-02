from code_intelligence.rag.prompt_builder import PromptBuilder


def test_prompt_builder():
    builder = PromptBuilder()
    prompt = builder.build(
        question="How does foo work?",
        repository_context="Rep context text",
        graph_context="Graph relationships text",
        conversation_context="Previous history text",
    )

    assert "How does foo work?" in prompt
    assert "Rep context text" in prompt
    assert "Graph relationships text" in prompt
    assert "Previous history text" in prompt
    assert "You are an expert AI Software Engineering Assistant." in prompt
