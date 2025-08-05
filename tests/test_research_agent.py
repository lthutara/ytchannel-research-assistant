

import os
import sys
import json
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import ResearchAgent

@pytest.fixture
def research_agent():
    """Provides a ResearchAgent instance for testing."""
    return ResearchAgent()

def test_research_agent_execution(research_agent):
    """
    Tests that the ResearchAgent runs and creates the expected artifacts.
    This test is for verifying the agent's process. The quality of the
    output should be manually inspected.
    """
    # 1. Setup
    topic = "The future of AI"
    output_dir = "artifacts"
    sources_path = os.path.join(output_dir, "sources.json")
    chunks_path = os.path.join(output_dir, "research_chunks.json")

    # Clean up previous run artifacts
    if os.path.exists(sources_path):
        os.remove(sources_path)
    if os.path.exists(chunks_path):
        os.remove(chunks_path)

    # 2. Execution
    research_agent.execute(topic)

    # 3. Verification
    assert os.path.exists(sources_path), "Research artifact (sources.json) was not created."
    assert os.path.exists(chunks_path), "Research chunks artifact (research_chunks.json) was not created."

    with open(sources_path, 'r') as f:
        sources_data = json.load(f)
        assert isinstance(sources_data, list)
        if sources_data:
            assert 'url' in sources_data[0]

    print("\n✅ Research Agent test passed successfully!")
    print(f"   - Verified {sources_path}")
    print(f"   - Verified {chunks_path}")
    print("   - Manual inspection of artifact quality is recommended.")

