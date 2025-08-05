

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

    # Clean up previous run artifacts if they exist
    if os.path.exists(sources_path):
        os.remove(sources_path)
    if os.path.exists(narrative_path):
        os.remove(narrative_path)

    # 2. Execution
    orchestrator = OrchestratorAgent()
    orchestrator.execute(topic)

    # 3. Verification
    assert os.path.exists(sources_path), "Research artifact (sources.json) was not created."
    assert os.path.exists(narrative_path), "Analysis artifact (narrative.md) was not created."

    print("\n✅ Stage 1 orchestration test passed successfully!")
    print(f"   - Verified {sources_path}")
    print(f"   - Verified {narrative_path}")


