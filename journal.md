# Project Journal: Content Weaver

## Initial Setup and Agent Implementation

### 1. Project Scaffolding
- Created the basic directory structure (`artifacts/` and `src/`).
- Created `requirements.txt` with the necessary Python packages (`langchain`, `langchain-google-genai`, `langchain-openai`, `requests`, `beautifulsoup4`, `python-dotenv`, `tavily-python`).
- Created a `.env` file for API keys and LLM provider selection.
- Defined a `BaseAgent` abstract class in `src/agents.py` (initially in `src/main.py`, then moved).

### 2. Implemented Core Agents
- **ResearchAgent:** Added to `src/agents.py`. This agent uses Tavily Search to find and scrape web content based on a given topic. It saves the raw sources to `artifacts/sources.json`.
- **AnalysisAgent:** Added to `src/agents.py`. This agent takes the research output (scraped content) and synthesizes it into a coherent narrative using an LLM. It saves the narrative to `artifacts/narrative.md`.

### 3. Environment Setup
- Created a Python virtual environment (`.venv`) using `python3 -m venv .venv`.
- Activated the virtual environment and installed all required dependencies using `pip install -r requirements.txt`.

### 4. Temporary Test Script
- Created a `main.py` script in the root directory to orchestrate and test the `ResearchAgent` and `AnalysisAgent` sequentially. This script prompts the user for a topic, runs the research, then runs the analysis, and prints the generated narrative.

### 5. Encountered Issues and Solutions

#### Issue 1: `pip` command not found
- **Context:** Initial attempt to install dependencies using `pip install -r requirements.txt` failed.
- **Solution:** Used `pip3 install -r requirements.txt` instead, as `pip` might not be directly in the PATH or linked to `python3`.

#### Issue 2: `EOFError: EOF when reading a line`
- **Context:** When running `python3 main.py`, the script expected interactive input for the topic, but the environment didn't provide it.
- **Solution:** Modified `main.py` to hardcode a default topic ("The future of AI") for testing purposes, removing the `input()` call.

#### Issue 3: `ModuleNotFoundError: No module named 'dotenv'`
- **Context:** After creating the virtual environment, `python3 main.py` failed because `python-dotenv` was not found.
- **Solution:** Activated the virtual environment using `source .venv/bin/activate` before running the script, ensuring that installed packages are accessible.

#### Issue 4: `ModuleNotFoundError: No module named 'langchain_community'`
- **Context:** Even after activating the virtual environment, `langchain_community` was not found.
- **Solution:** Explicitly installed `langchain-community` within the activated virtual environment using `pip install langchain-community`.

#### Issue 5: `ValueError: LLM_PROVIDER must be 'GOOGLE' or 'OPENAI'`
- **Context:** The `_get_llm` method in `ResearchAgent` and `AnalysisAgent` raised an error because the `LLM_PROVIDER` environment variable was not set in the `.env` file.
- **Solution:** Added `LLM_PROVIDER="OPENAI"` to the `.env` file to explicitly specify the LLM provider.

#### Issue 6: `openai.RateLimitError: Request too large for gpt-4` (Initial Attempt)
- **Context:** The `AnalysisAgent` failed because the `full_content` (joined research chunks) exceeded the token limit for the GPT-4 model.
- **Solution:** Implemented a `_summarize_chunks` method in `AnalysisAgent` to summarize each research chunk individually before sending them to the LLM for narrative generation.

#### Issue 7: `openai.RateLimitError: Request too large for gpt-4` (Persistent)
- **Context:** Even after summarizing individual chunks, the combined summaries were still too large for the GPT-4 model's token limit.
- **Solution:** Implemented a limit on the number of chunks processed for summarization (`max_chunks_to_process = 50`) within the `_summarize_chunks` method of `AnalysisAgent`. This significantly reduced the input token count, resolving the `RateLimitError`.

### 6. Current Status
- The `ResearchAgent` successfully fetches and chunks web content.
- The `AnalysisAgent` successfully summarizes the chunks and generates a narrative, saving it to `artifacts/narrative.md`.
- The temporary `main.py` script successfully orchestrates these two agents.

### 7. Next Steps
- Implement the `Orchestrator Agent` as per the `implementation.md` plan.

## Feature 3: Orchestration & Content Generation

### PR #4: `feat: Implement Orchestrator Agent`
- **Context:** With the `ResearchAgent` and `AnalysisAgent` successfully implemented and tested, the next logical step was to create the `OrchestratorAgent`. This agent serves as the central director, managing the workflow by calling other agents in the correct sequence and handling data flow between them.
- **Action:** Implemented the `OrchestratorAgent` in `src/agents.py`. This agent initializes `ResearchAgent` and `AnalysisAgent` instances and orchestrates their execution: first, it calls the `ResearchAgent` to gather content, and then it passes the research output to the `AnalysisAgent` to generate a narrative.
- **Outcome:** The `OrchestratorAgent` successfully orchestrated the research and analysis process, generating a coherent narrative and saving it to `artifacts/narrative.md`. The previous `RateLimitError` was resolved by limiting the number of chunks processed during summarization.

### 8. Next Steps
- Implement the `Scriptwriting Agent` (PR #5).
- Implement the `ArticleWriter Agent` (PR #6).
- Implement the `Visual Asset Agent` (PR #7).
