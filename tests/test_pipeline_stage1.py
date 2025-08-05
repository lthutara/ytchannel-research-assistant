

import os
import sys
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import OrchestratorAgent

def test_stage1_orchestration():
    """
    Tests the initial pipeline (Research -> Analysis) to ensure it runs and
    produces the expected artifacts.
    """
    # 1. Setup
    topic = "The future of AI"
    output_dir = "artifacts"
    sources_path = os.path.join(output_dir, "sources.json")
    narrative_path = os.path.join(output_dir, "narrative.md")
    script_path = os.path.join(output_dir, "script.md")
    article_path = os.path.join(output_dir, "article.md")

    # Clean up previous run artifacts if they exist
    if os.path.exists(sources_path):
        os.remove(sources_path)
    if os.path.exists(narrative_path):
        os.remove(narrative_path)
    if os.path.exists(script_path):
        os.remove(script_path)
    if os.path.exists(article_path):
        os.remove(article_path)

    # 2. Execution
    orchestrator = OrchestratorAgent()
    result = orchestrator.execute(topic, simulate_llm_calls=True)

    # 3. Verification
    assert os.path.exists(sources_path), "Research artifact (sources.json) was not created."
    assert os.path.exists(narrative_path), "Analysis artifact (narrative.md) was not created."
    assert os.path.exists(script_path), "Scriptwriting artifact (script.md) was not created."
    assert os.path.exists(article_path), "ArticleWriter artifact (article.md) was not created."

    # Verify content of simulated files
    with open(narrative_path, 'r') as f:
        assert "Simulated Narrative" in f.read()
    with open(script_path, 'r') as f:
        assert "Simulated Video Script" in f.read()
    with open(article_path, 'r') as f:
        assert "Simulated Web Article" in f.read()

    # Verify token usage is present (even if simulated to 0)
    assert "token_usage" in result
    assert "analysis" in result["token_usage"]
    assert "scriptwriting" in result["token_usage"]
    assert "article_writing" in result["token_usage"]

    print("\n✅ Stage 1 orchestration test passed successfully with simulated LLM calls!")
    print(f"   - Verified {sources_path}")
    print(f"   - Verified {narrative_path}")
    print(f"   - Verified {script_path}")
    print(f"   - Verified {article_path}")
    print(f"   - Verified token usage: {result["token_usage"]}")


