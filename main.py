from src.agents import ResearchAgent, AnalysisAgent
import os

def main():
    topic = "The future of AI" # Hardcoded for testing purposes

    # Initialize and run ResearchAgent
    research_agent = ResearchAgent()
    research_content = research_agent.execute(topic)

    # Initialize and run AnalysisAgent
    analysis_agent = AnalysisAgent()
    narrative = analysis_agent.execute(research_content)

    print("\n--- Generated Narrative ---")
    print(narrative)

if __name__ == "__main__":
    main()

