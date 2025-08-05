

import os
import sys
import pytest
import json
from langchain_core.runnables import Runnable

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import VisualAssetAgent

# Create a Mock LLM class that is a valid Runnable
class MockLLM(Runnable):
    """A fake LLM that returns a predictable response for testing."""
    def invoke(self, *args, **kwargs):
        # Mock the .content attribute that the real LLM response has
        mock_json_content = {
            "introduction": ["stock footage of AI concepts", "futuristic cityscapes"],
            "act_1": ["brain-computer interface diagrams", "robotics in action"],
            "act_2": ["ethical dilemma illustrations", "data privacy icons"],
            "conclusion": ["diverse group of people collaborating", "sustainable tech imagery"]
        }
        class MockContent:
            content = json.dumps(mock_json_content)
            response_metadata = {"token_usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}} # Add dummy token usage
        return MockContent()

@pytest.fixture
def visual_asset_agent():
    """Provides a VisualAssetAgent instance for testing."""
    return VisualAssetAgent()

@pytest.fixture
def video_script_fixture():
    """Provides a sample video script for the visual asset agent."""
    script_path = "artifacts/script.md"
    if not os.path.exists(script_path):
        # Create a placeholder if it doesn't exist
        placeholder_content = "# Sample Video Script\n\nThis is a placeholder video script for visual asset testing."
        with open(script_path, "w") as f:
            f.write(placeholder_content)
    
    with open(script_path, 'r') as f:
        return f.read()

def test_visual_asset_agent_execution(visual_asset_agent, video_script_fixture, monkeypatch):
    """
    Tests that the VisualAssetAgent runs and creates the shotlist artifact.
    This test uses a mock LLM to avoid API calls.
    """
    # Use monkeypatch to replace the real LLM with our mock
    monkeypatch.setattr(visual_asset_agent, 'llm', MockLLM())

    # Setup
    output_dir = "artifacts"
    shotlist_path = os.path.join(output_dir, "shotlist.json")

    # Clean up previous run artifact
    if os.path.exists(shotlist_path):
        os.remove(shotlist_path)

    # Execution
    visual_asset_agent.execute(video_script_fixture)

    # Verification
    assert os.path.exists(shotlist_path), "VisualAsset artifact (shotlist.json) was not created."

    # Verify the content of the created file
    with open(shotlist_path, 'r') as f:
        content = json.load(f)
        expected_content = {
            "introduction": ["stock footage of AI concepts", "futuristic cityscapes"],
            "act_1": ["brain-computer interface diagrams", "robotics in action"],
            "act_2": ["ethical dilemma illustrations", "data privacy icons"],
            "conclusion": ["diverse group of people collaborating", "sustainable tech imagery"]
        }
        assert content == expected_content

    print("\n✅ VisualAsset Agent test passed successfully with a mock LLM!")
    print(f"   - Verified {shotlist_path} was created with the correct mock content.")

