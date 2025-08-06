
## Sarvam AI Integration & LLM Clarifications (August 6, 2025)

### 1. Sarvam AI Integration
- **Context:** Explored integrating Sarvam AI as an alternative LLM provider. Initial attempts with direct `SarvamAI` client were incompatible with LangChain's `Runnable` interface.
- **Solution:** Configured `langchain_openai.ChatOpenAI` to work with Sarvam AI's OpenAI-compatible API.
    - Updated `src/agents.py` to use `openai_api_base="https://api.sarvam.ai/v1/"` and `openai_api_key=os.getenv("api_subscription_key")` with `model="sarvam-m"` when `LLM_PROVIDER` is set to `"SARVAM"`.
    - Added `sarvamai` to `requirements.txt` (though the direct `SarvamAI` client was not used, the library might contain necessary underlying components or dependencies for the OpenAI-compatible API).
- **Testing:** Created `test_sarvam_integration.py` to verify the integration.
- **Issue Encountered:** Initially faced "Subscription not found" (403) and "Rate limit exceeded" (429) errors.
- **Resolution:** The 403 error was due to an inactive subscription or model access. The 429 error was mitigated by reducing `max_chunks_to_process` in `AnalysisAgent` and implicitly by the sequential nature of the calls.
- **Outcome:** Successfully ran `test_sarvam_integration.py`, confirming that LangChain can now use Sarvam AI via its OpenAI-compatible API.

### 2. Clarification on Embedding Models
- **Current Project Scope:** The "Content Weaver" project does not currently require an embedding model. Its workflow involves gathering information via web search and then processing/generating text directly with LLMs. There are no semantic search, RAG, or content recommendation features implemented that would necessitate embeddings.
- **When Embeddings are Needed:** Embedding models are crucial for tasks like:
    - **Retrieval Augmented Generation (RAG):** For semantically searching a knowledge base to retrieve relevant information before LLM generation.
    - **Semantic Search:** Finding documents or content based on meaning, not just keywords.
    - **Content Clustering/Recommendation:** Grouping or suggesting content based on semantic similarity.

### 3. Clarification on Chunking
- **Current Use:** In the `AnalysisAgent`, chunking is used solely to manage LLM token limits. Large scraped texts are broken into smaller chunks, each summarized individually by the LLM, and then combined to form the narrative. This is a technical necessity for LLM interaction, not a step towards generating embeddings.
- **Chunking with Embeddings:** If embedding models were to be introduced, chunking would be a preliminary step to prepare text for embedding generation, where each chunk would be converted into a numerical vector representing its semantic meaning.
