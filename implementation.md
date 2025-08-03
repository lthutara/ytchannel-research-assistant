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

## 2. Implementation Steps (PRs)

### Feature 1: Project Scaffolding
#### PR #1: `feat: Initial project setup and agent interface`
*   **Description:** Establishes the foundational directory structure, dependencies (`langchain`, `langchain-google-genai`, `langchain-openai`, `requests`, `beautifulsoup4`, `python-dotenv`), and a `BaseAgent` abstract class.

### Feature 2: Core Research & Narrative Generation
#### PR #2: `feat: Implement Research Agent`
*   **Description:** Implements the "Librarian" agent to fetch and scrape raw data, producing `artifacts/sources.json`.

#### PR #3: `feat: Implement Analysis Agent`
*   **Description:** Implements the "Storyteller" agent to synthesize a narrative, producing `artifacts/narrative.md`.
*   **Details:** The agent will dynamically select its LLM (Gemini or OpenAI) based on the `LLM_PROVIDER` environment variable.

### Feature 3: Orchestration & Content Generation
#### PR #4: `feat: Implement Orchestrator Agent`
*   **Description:** Implements the "Director" agent to manage the workflow, chaining the Research and Analysis agents.

#### PR #5: `feat: Implement Scriptwriting Agent`
*   **Description:** Adds the "Video Writer" agent to the pipeline, producing `artifacts/script.md`.
*   **Details:** The agent will dynamically select its LLM.

#### PR #6: `feat: Implement ArticleWriter Agent`
*   **Description:** Adds the "Blog Writer" agent to the pipeline, producing `artifacts/article.md`.
*   **Details:** The agent will dynamically select its LLM.

### Feature 4: Final Polish & Completion
#### PR #7: `feat: Implement Visual Asset Agent`
*   **Description:** Completes the pipeline by adding the "Art Director" agent, producing `artifacts/shotlist.json`.
*   **Details:** The agent will dynamically select its LLM.
