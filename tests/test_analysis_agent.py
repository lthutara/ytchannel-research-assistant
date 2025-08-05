

import os
import sys
import json
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import AnalysisAgent, ResearchAgent

@pytest.fixture
def analysis_agent():
    """Provides an AnalysisAgent instance for testing."""
    return AnalysisAgent()

@pytest.fixture
def research_chunks_fixture():
    """
    Provides research chunks for the analysis agent, either by running the
    ResearchAgent or by loading from a cached file.
    """
    output_dir = "artifacts"
    chunks_path = os.path.join(output_dir, "research_chunks.json")

    # If cached chunks exist, load them to save time and tokens
    if os.path.exists(chunks_path):
        print("\nLoading cached research chunks...")
        with open(chunks_path, 'r') as f:
            return json.load(f)
    else:
        # If no cache, run the ResearchAgent to generate them
        print("\nNo cached chunks found. Running ResearchAgent to generate them...")
        research_agent = ResearchAgent()
        return research_agent.execute("The future of AI")

def test_analysis_agent_execution(analysis_agent, research_chunks_fixture):
    """
    Tests that the AnalysisAgent runs and creates the narrative artifact.
    This test uses cached research data if available.
    """
    # 1. Setup
    output_dir = "artifacts"
    narrative_path = os.path.join(output_dir, "narrative.md")

    # Clean up previous run artifact
    if os.path.exists(narrative_path):
        os.remove(narrative_path)

    # 2. Execution
    analysis_agent.execute(research_chunks_fixture)

    # 3. Verification
    assert os.path.exists(narrative_path), "Analysis artifact (narrative.md) was not created."

    print("\n✅ Analysis Agent test passed successfully!")
    print(f"   - Verified {narrative_path}")
    print("   - Manual inspection of artifact quality is recommended.")

