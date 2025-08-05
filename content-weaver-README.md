# Content Weaver: An AI-Powered Content Creation Framework

## 1. Project Vision

Content Weaver is a multi-agent, programmatic framework designed to automate the creation of content packages from a single topic. It ingests a topic and produces a "ready-to-use" package containing a video script, a web article, and a list of suggested visual assets.

The primary goal of this project is to build a robust, configurable, and extensible "content factory" that can dramatically reduce the time required to produce high-quality first drafts.

This project was initially planned within the `my-project-ideas` repository under the "tech-voice-youtube" idea.

## 2. Core Documentation

The detailed planning for this framework has already been completed. The core documents that guide its implementation are:

*   **System Design Document (`docs/design.md`):** This document contains the high-level vision, architectural diagrams, and detailed descriptions of each agent's role and responsibility. It is the "what" and "why" of the project.

*   **Implementation Plan (`docs/implementation.md`):** This document provides a concrete, step-by-step action plan for building the framework, broken down into a series of Pull Requests (PRs). It is the "how" of the project.

## 3. Getting Started & Development Workflow

To begin development or to get the project running, follow these steps:

1.  **Review the Core Documentation:** Start by reading the `design.md` and `implementation.md` files to fully understand the project's architecture and development roadmap.

2.  **Set up the Environment:**
    *   Create a `.env` file in the project root.
    *   Add your API keys for your chosen LLM provider (Google Gemini or OpenAI) and the Tavily Search API, as detailed in the `implementation.md`.

3.  **Install Dependencies:**
    *   Install all required Python packages using the `requirements.txt` or `pyproject.toml` file.

4.  **Development Workflow: "Develop, Test, Move"**
    We follow an iterative development approach to ensure reliability, efficiency, and cost-effectiveness. Each agent and feature is developed and tested in isolation before being integrated into the main pipeline. This minimizes API calls during development and allows for focused debugging.
    *   **Isolated Development:** New agents are built and tested using dedicated test scripts that leverage cached or mocked data from previous stages.
    *   **Comprehensive Testing:** Both unit tests (for individual agents) and integration tests (for the full pipeline) are maintained in the `tests/` directory.
    *   **Simulated Runs:** The `OrchestratorAgent` supports a `simulate_llm_calls` flag, enabling full end-to-end pipeline runs without incurring LLM API costs, crucial for rapid iteration and testing.

    For detailed steps, current development status, and future enhancements, please refer to `implementation.md` and `journal.md`.
