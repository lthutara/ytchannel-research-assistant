from src.agents import OrchestratorAgent

def main():
    topic = "The future of AI"  # Hardcoded for testing purposes

    orchestrator = OrchestratorAgent()
    narrative = orchestrator.execute(topic)

    print("\n--- Final Narrative ---")
    print(narrative)

if __name__ == "__main__":
    main()
