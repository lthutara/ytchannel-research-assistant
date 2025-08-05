# Implementation Plan: "Content Weaver"

This document breaks down the development of the Content Weaver framework into a series of features and corresponding Pull Requests (PRs).

---

## 1. Prerequisites & Configuration

This framework is designed to be flexible, allowing you to choose your LLM provider. Configuration is managed via environment variables.

### 1.1. API Keys & Environment Setup
Create a `.env` file in the project root. The application will load these variables to configure itself.

```
# .env file

# --- Core Configuration ---
# Choose your LLM provider: "GOOGLE" or "OPENAI"
LLM_PROVIDER="GOOGLE"

# --- API Keys ---
# Google AI API Key (for Gemini models)
GOOGLE_API_KEY="your-google-api-key"

# OpenAI API Key (for GPT models)
OPENAI_API_KEY="your-openai-api-key"

# Tavily Search API Key (for the Research Agent)
TAVILY_API_KEY="your-tavily-api-key"
```

### 1.2. Dynamic LLM Selection
The application code will read the `LLM_PROVIDER` variable:
- If set to `"GOOGLE"`, the agents will use the `ChatGoogleGenerativeAI` model from LangChain.
- If set to `"OPENAI"`, the agents will use the `ChatOpenAI` model.
This allows you to switch between LLM providers without changing any code.

---

## 3. Testing Strategy

To ensure the reliability and stability of the Content Weaver framework, we will follow a "Develop, Test, Move" strategy. Each new feature will be developed in isolation and accompanied by tests before being integrated into the main pipeline.

-   **Unit and Integration Tests:** Tests for each agent and for the integrated pipeline will be located in the `tests/` directory.
-   **Running Tests:** Tests can be executed using `pytest` from the root of the project.

---

---

## 2. Implementation Steps (PRs)

### Feature 1: Project Scaffolding
#### PR #1: `feat: Initial project setup and agent interface`
*   **Description:** Establishes the foundational directory structure, dependencies (`langchain`, `langchain-google-genai`, `langchain-openai`, `requests`, `beautifulsoup4`, `python-dotenv`), and a `BaseAgent` abstract class.
*   **Status:** Completed.

### Feature 2: Core Research & Narrative Generation
#### PR #2: `feat: Implement Research Agent`
*   **Description:** Implements the "Librarian" agent to fetch and scrape raw data, producing `artifacts/sources.json`.
*   **Status:** Completed.

#### PR #3: `feat: Implement Analysis Agent`
*   **Description:** Implements the "Storyteller" agent to synthesize a narrative, producing `artifacts/narrative.md`.
*   **Details:** The agent will dynamically select its LLM (Gemini or OpenAI) based on the `LLM_PROVIDER` environment variable.
*   **Status:** Completed.

### Feature 3: Orchestration & Content Generation
#### PR #4: `feat: Implement Orchestrator Agent`
*   **Description:** Implements the "Director" agent to manage the workflow, chaining the Research and Analysis agents.
*   **Status:** Completed.

#### PR #5: `feat: Implement Scriptwriting Agent`
*   **Description:** Adds the "Video Writer" agent to the pipeline, producing `artifacts/script.md`.
*   **Details:** The agent will dynamically select its LLM.
*   **Status:** Completed.

#### PR #6: `feat: Implement ArticleWriter Agent`
*   **Description:** Adds the "Blog Writer" agent to the pipeline, producing `artifacts/article.md`.
*   **Details:** The agent will dynamically select its LLM.
*   **Status:** Completed.

### Feature 4: Final Polish & Completion
#### PR #7: `feat: Implement Visual Asset Agent`
*   **Description:** Completes the pipeline by adding the "Art Director" agent, producing `artifacts/shotlist.json`.
*   **Details:** The agent will dynamically select its LLM.
*   **Status:** Completed.

---

## 4. Future Enhancements

These are potential features and improvements that can be added to the Content Weaver framework in future development cycles.

### Feature 5: Selective Content Generation
*   **Description:** Allow the user to specify which content types (e.g., video script, web article, visual assets) should be generated. This will involve modifying the `OrchestratorAgent` to accept parameters for selective execution, enabling more flexible and efficient content creation based on specific user needs.

### Feature 6: Multilingual Output (Telugu)
*   **Description:** Implement the capability to generate final content (video script, web article) in Telugu. This will require careful prompt engineering for the LLMs to ensure accurate and idiomatic translation, and may involve integrating language translation tools if direct LLM generation proves insufficient or too costly.