# System Design: "Content Weaver"

## 1. Overview

"Content Weaver" is a multi-agent, programmatic framework designed to automate the creation of content packages from a single topic. It ingests a topic and produces a "ready-to-use" package containing a video script, a web article, and a list of suggested visual assets for the video. The system is designed for minimal human intervention, acting as a "content factory" to streamline production.

## 2. Guiding Principles & Success Metrics

*   **Modularity:** Each agent should be a self-contained component that can be tested and improved independently.
*   **Configurability:** Prompts, API keys, and core settings should be managed via configuration files, not hardcoded.
*   **Success Metric:** A successful run of the framework will produce a "script package" that is 80% complete, requiring only minor human polish before production.
*   **Key Performance Indicator:** Reduce the time to create a first-draft script package from hours to minutes.

## 3. Architectural Diagram

The system operates as a pipeline, where the output of one agent becomes the input for the next. The Orchestrator manages the flow, and the content generation for the script and article can happen in parallel.

```
[User Input: topic.txt]
         |
         v
+--------------------+
| Orchestrator Agent |
+--------------------+
         |
         | 1. Executes Research
         v
+--------------------+
|   Research Agent   | --> [artifacts/sources.json]
+--------------------+
         |
         | 2. Executes Analysis
         v
+--------------------+
|   Analysis Agent   | --> [artifacts/narrative.md]
+--------------------+
         |
         | 3. Executes Content Generation (in parallel)
+--------+---------+
|                  |
v                  v
+------------------+  +-------------------+
| Scriptwriting    |  |  ArticleWriter    |
|      Agent       |  |       Agent       |
+------------------+  +-------------------+
|                  |
|                  v
v                  [artifacts/article.md]
[artifacts/script.md]
|
| 4. Executes Visual Suggestion
v
+------------------+
|  Visual Asset    | --> [artifacts/shotlist.json]
|      Agent       |
+------------------+
         |
         v
[Final Content Package]
```

## 4. Component Descriptions

*   **Orchestrator Agent (The "Director"):** Manages the entire workflow. It takes the initial topic, calls the other agents in the correct sequence, and handles the passing of data artifacts between them.

*   **Research Agent (The "Librarian"):** Gathers raw information from the web.
    *   **Input:** A string containing the topic.
    *   **Output:** A JSON file (`sources.json`) containing a list of URLs and their scraped text content.

*   **Analysis Agent (The "Storyteller"):** Synthesizes the raw data from the Research Agent into a coherent narrative. This is the core creative engine of the system.
    *   **Input:** `sources.json`.
    *   **Output:** A Markdown file (`narrative.md`) outlining the story's core themes, acts, and key data points.

*   **Scriptwriting Agent (The "Video Writer"):** Transforms the structured narrative into a conversational, engaging video script, adopting the specific "Tech Voice" persona.
    *   **Input:** `narrative.md`.
    *   **Output:** A Markdown file (`script.md`).

*   **ArticleWriter Agent (The "Blog Writer"):** Transforms the same narrative into a well-structured, long-form article suitable for a website or blog.
    *   **Input:** `narrative.md`.
    *   **Output:** A Markdown file (`article.md`).

*   **Visual Asset Agent (The "Art Director"):** Reads the final video script and suggests appropriate visuals (e.g., diagrams, photos, stock footage) for each section.
    *   **Input:** `script.md`.
    *   **Output:** A JSON file (`shotlist.json`) mapping script sections to visual ideas.

## 5. Assumptions and Error Handling

*   **Assumptions:**
    *   The system has stable internet access.
    *   API keys for LLMs and search tools are valid and provided via a `.env` file.
    *   The websites to be scraped are renderable without JavaScript-heavy clients.
*   **Error Handling Strategy:**
    *   The Orchestrator is responsible for basic error handling.
    *   If any agent in the pipeline fails, the Orchestrator will halt execution and log a clear error message indicating which agent failed and why.
    *   The Research Agent will include a timeout for web requests and will skip any URL that fails to load after a reasonable number of retries.
