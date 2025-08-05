

import os
import sys
import pytest
from langchain_core.runnables import Runnable

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import ArticleWriterAgent

# Create a Mock LLM class that is a valid Runnable
class MockLLM(Runnable):
    """A fake LLM that returns a predictable response for testing."""
    def invoke(self, *args, **kwargs):
        # Mock the .content attribute that the real LLM response has
        class MockContent:
            content = "This is a mock article."
        return MockContent()

@pytest.fixture
def article_writer_agent():
    """Provides an ArticleWriterAgent instance for testing."""
    return ArticleWriterAgent()

@pytest.fixture
def narrative_fixture():
    """Provides a sample narrative for the article writer agent."""
    narrative_path = "artifacts/narrative.md"
    if not os.path.exists(narrative_path):
        # Create a placeholder if it doesn't exist
        placeholder_content = "# The Future of AI\n\nThis is a placeholder narrative for the article."
        with open(narrative_path, "w") as f:
            f.write(placeholder_content)
    
    with open(narrative_path, 'r') as f:
        return f.read()

def test_article_writer_agent_execution(article_writer_agent, narrative_fixture, monkeypatch):
    """
    Tests that the ArticleWriterAgent runs and creates the article artifact.
    This test uses a mock LLM to avoid API calls.
    """
    # Use monkeypatch to replace the real LLM with our mock
    monkeypatch.setattr(article_writer_agent, 'llm', MockLLM())

    # Setup
    output_dir = "artifacts"
    article_path = os.path.join(output_dir, "article.md")

    # Clean up previous run artifact
    if os.path.exists(article_path):
        os.remove(article_path)

    # Execution
    article_writer_agent.execute(narrative_fixture)

    # Verification
    assert os.path.exists(article_path), "ArticleWriter artifact (article.md) was not created."

    # Verify the content of the created file
    with open(article_path, 'r') as f:
        content = f.read()
        assert content == "This is a mock article."

    print("\n✅ ArticleWriter Agent test passed successfully with a mock LLM!")
    print(f"   - Verified {article_path} was created with the correct mock content.")

