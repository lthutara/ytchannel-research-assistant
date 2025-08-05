
import os
import sys
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import ScriptwritingAgent

from langchain_core.runnables import Runnable

# 1. Create a Mock LLM class that is a valid Runnable
class MockLLM(Runnable):
    """A fake LLM that returns a predictable response for testing."""
    def invoke(self, *args, **kwargs):
        # Mock the .content attribute that the real LLM response has
        class MockContent:
            content = "This is a mock script."
        return MockContent()

@pytest.fixture
def scriptwriting_agent():
    """Provides a ScriptwritingAgent instance for testing."""
    return ScriptwritingAgent()

@pytest.fixture
def narrative_fixture():
    """Provides a sample narrative for the scriptwriting agent."""
    narrative_path = "artifacts/narrative.md"
    if not os.path.exists(narrative_path):
        placeholder_content = "# The Future of AI\n\nThis is a placeholder narrative."
        with open(narrative_path, "w") as f:
            f.write(placeholder_content)
    
    with open(narrative_path, 'r') as f:
        return f.read()

def test_scriptwriting_agent_execution(scriptwriting_agent, narrative_fixture, monkeypatch):
    """
    Tests that the ScriptwritingAgent runs and creates the script artifact.
    This test uses a mock LLM to avoid API calls.
    """
    # 2. Use monkeypatch to replace the real LLM with our mock
    monkeypatch.setattr(scriptwriting_agent, 'llm', MockLLM())

    # 3. Setup
    output_dir = "artifacts"
    script_path = os.path.join(output_dir, "script.md")

    # Clean up previous run artifact
    if os.path.exists(script_path):
        os.remove(script_path)

    # 4. Execution
    scriptwriting_agent.execute(narrative_fixture)

    # 5. Verification
    assert os.path.exists(script_path), "Scriptwriting artifact (script.md) was not created."

    # Verify the content of the created file
    with open(script_path, 'r') as f:
        content = f.read()
        assert content == "This is a mock script."

    print("\n✅ Scriptwriting Agent test passed successfully with a mock LLM!")
    print(f"   - Verified {script_path} was created with the correct mock content.")
