from abc import ABC, abstractmethod
import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import requests

load_dotenv()

class BaseAgent(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class ResearchAgent(BaseAgent):
    def __init__(self):
        self.llm = self._get_llm()
        self.web_search_tool = TavilySearch(max_results=5)

    def _get_llm(self):
        llm_provider = os.getenv("LLM_PROVIDER")
        if llm_provider == "GOOGLE":
            return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        elif llm_provider == "OPENAI":
            return ChatOpenAI(model="gpt-4", temperature=0.7)
        elif llm_provider == "SARVAM":
            return ChatOpenAI(
                openai_api_base="https://api.sarvam.ai/v1/",
                openai_api_key=os.getenv("api_subscription_key"), # Sarvam uses OpenAI-compatible API key
                model="sarvam-m", # You might need to specify the exact model name here
                temperature=0.7
            )
        else:
            raise ValueError("LLM_PROVIDER must be 'GOOGLE', 'OPENAI', or 'SARVAM'")

    def _scrape_and_chunk(self, urls):
        all_content = []
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()
                all_content.append(text)
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_text(" ".join(all_content))
        return chunks

    def _generate_topic_id(self, topic: str) -> str:
        """Generate consistent topic_id from topic string."""
        topic_id = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
        topic_id = re.sub(r'[\s-]+', '-', topic_id).strip('-')
        return topic_id

    def execute(self, topic: str):
        print(f"Researching topic: {topic}")
        search_results = self.web_search_tool.invoke(topic)
        urls = [result['url'] for result in search_results['results']]
        print(f"Found URLs: {urls}")
        
        scraped_content_chunks = self._scrape_and_chunk(urls)
        
        sources_data = []
        for i, url in enumerate(urls):
            sources_data.append({
                "url": url,
                "content_preview": scraped_content_chunks[i][:500] if scraped_content_chunks else "No content scraped"
            })

        # Use topic-specific directory with consistent topic_id generation
        topic_id = self._generate_topic_id(topic)
        output_dir = f"artifacts/{topic_id}"
        os.makedirs(output_dir, exist_ok=True)
        sources_output_path = os.path.join(output_dir, "sources.json")
        chunks_output_path = os.path.join(output_dir, "research_chunks.json")

        with open(sources_output_path, "w") as f:
            json.dump(sources_data, f, indent=4)

        with open(chunks_output_path, "w") as f:
            json.dump(scraped_content_chunks, f, indent=4)

        print(f"Research complete. Sources saved to {sources_output_path}")
        return scraped_content_chunks

class AnalysisAgent(BaseAgent):
    def __init__(self):
        self.llm = self._get_llm()

    def _get_llm(self):
        llm_provider = os.getenv("LLM_PROVIDER")
        if llm_provider == "GOOGLE":
            return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        elif llm_provider == "OPENAI":
            return ChatOpenAI(model="gpt-4", temperature=0.7)
        elif llm_provider == "SARVAM":
            return ChatOpenAI(
                openai_api_base="https://api.sarvam.ai/v1/",
                openai_api_key=os.getenv("api_subscription_key"), # Sarvam uses OpenAI-compatible API key
                model="sarvam-m", # You might need to specify the exact model name here
                temperature=0.7
            )
        else:
            raise ValueError("LLM_PROVIDER must be 'GOOGLE', 'OPENAI', or 'SARVAM'")

    def _generate_topic_id(self, topic: str) -> str:
        """Generate consistent topic_id from topic string."""
        topic_id = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
        topic_id = re.sub(r'[\s-]+', '-', topic_id).strip('-')
        return topic_id

    def execute(self, research_content_chunks: list, topic: str):
        print("Analyzing research content...")
        template = """You are an expert content analyst. Your task is to synthesize the provided research content into a coherent and engaging narrative. 
        Focus on the core themes, key data points, and a logical flow that would be suitable for a video script and a web article.

        Research Content:
        {research_content}

        Please provide the narrative in Markdown format, outlining the story's core themes, acts, and key data points.
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm

        summarized_content = self._summarize_chunks(research_content_chunks)
        
        narrative_response = chain.invoke({"research_content": summarized_content})
        narrative_content = narrative_response.content
        token_usage = narrative_response.response_metadata.get("token_usage", {})

        # Use topic-specific directory with consistent topic_id generation
        topic_id = self._generate_topic_id(topic)
        output_dir = f"artifacts/{topic_id}"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "narrative.md")
        
        with open(output_path, "w") as f:
            f.write(narrative_content)
        
        print(f"Analysis complete. Narrative saved to {output_path}")
        return {"content": narrative_content, "token_usage": token_usage}

    def _summarize_chunks(self, chunks: list):
        print("Summarizing research chunks...")
        summaries = []
        summary_template = """Please provide a concise summary of the following text:

{text}

Summary:"""
        summary_prompt = ChatPromptTemplate.from_template(summary_template)
        summary_chain = summary_prompt | self.llm

        # Limit the number of chunks to process to avoid rate limits
        max_chunks_to_process = 5  # Reduced for testing rate limits
        import time # Import time for sleep
        for i, chunk in enumerate(chunks[:max_chunks_to_process]):
            try:
                summary = summary_chain.invoke({"text": chunk})
                summaries.append(summary.content)
                print(f"Summarized chunk {i+1}/{len(chunks)}")
            except Exception as e:
                print(f"Error summarizing chunk {i+1}: {e}")
                summaries.append("Error summarizing chunk.") # Add a placeholder for failed summaries
        
        return "\n\n".join(summaries)

class ScriptwritingAgent(BaseAgent):
    def __init__(self):
        self.llm = self._get_llm()

    def _get_llm(self):
        llm_provider = os.getenv("LLM_PROVIDER")
        if llm_provider == "GOOGLE":
            return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        elif llm_provider == "OPENAI":
            return ChatOpenAI(model="gpt-4", temperature=0.7)
        elif llm_provider == "SARVAM":
            return ChatOpenAI(
                openai_api_base="https://api.sarvam.ai/v1/",
                openai_api_key=os.getenv("api_subscription_key"), # Sarvam uses OpenAI-compatible API key
                model="sarvam-m", # You might need to specify the exact model name here
                temperature=0.7
            )
        else:
            raise ValueError("LLM_PROVIDER must be 'GOOGLE', 'OPENAI', or 'SARVAM'")

    def _generate_topic_id(self, topic: str) -> str:
        """Generate consistent topic_id from topic string."""
        topic_id = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
        topic_id = re.sub(r'[\s-]+', '-', topic_id).strip('-')
        return topic_id

    def execute(self, narrative: str, topic: str):
        print("Generating video script...")
        template = """You are an expert video scriptwriter. Your task is to transform the provided narrative into a conversational and engaging video script.
        The script should be suitable for a 'tech voice' YouTube channel.

        Narrative:
        {narrative}

        Please provide the video script in Markdown format, including sections for introduction, main points, and conclusion.
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm

        video_script_response = chain.invoke({"narrative": narrative})
        video_script_content = video_script_response.content
        token_usage = video_script_response.response_metadata.get("token_usage", {})

        # Use topic-specific directory with consistent topic_id generation
        topic_id = self._generate_topic_id(topic)
        output_dir = f"artifacts/{topic_id}"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "script.md")
        
        with open(output_path, "w") as f:
            f.write(video_script_content)
        
        print(f"Video script generated and saved to {output_path}")
        return {"content": video_script_content, "token_usage": token_usage}

class ArticleWriterAgent(BaseAgent):
    def __init__(self):
        self.llm = self._get_llm()

    def _get_llm(self):
        llm_provider = os.getenv("LLM_PROVIDER")
        if llm_provider == "GOOGLE":
            return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        elif llm_provider == "OPENAI":
            return ChatOpenAI(model="gpt-4", temperature=0.7)
        elif llm_provider == "SARVAM":
            return ChatOpenAI(
                openai_api_base="https://api.sarvam.ai/v1/",
                openai_api_key=os.getenv("api_subscription_key"), # Sarvam uses OpenAI-compatible API key
                model="sarvam-m", # You might need to specify the exact model name here
                temperature=0.7
            )
        else:
            raise ValueError("LLM_PROVIDER must be 'GOOGLE', 'OPENAI', or 'SARVAM'")

    def _generate_topic_id(self, topic: str) -> str:
        """Generate consistent topic_id from topic string."""
        topic_id = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
        topic_id = re.sub(r'[\s-]+', '-', topic_id).strip('-')
        return topic_id

    def execute(self, narrative: str, topic: str):
        print("Generating web article...")
        template = """You are an expert article writer. Your task is to transform the provided narrative into a well-structured, long-form article suitable for a website or blog.

        Narrative:
        {narrative}

        Please provide the article in Markdown format, including a clear title, headings, and subheadings.
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm

        web_article_response = chain.invoke({"narrative": narrative})
        web_article_content = web_article_response.content
        token_usage = web_article_response.response_metadata.get("token_usage", {})

        # Use topic-specific directory with consistent topic_id generation
        topic_id = self._generate_topic_id(topic)
        output_dir = f"artifacts/{topic_id}"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "article.md")
        
        with open(output_path, "w") as f:
            f.write(web_article_content)
        
        print(f"Web article generated and saved to {output_path}")
        return {"content": web_article_content, "token_usage": token_usage}

class VisualAssetAgent(BaseAgent):
    def __init__(self):
        self.llm = self._get_llm()

    def _get_llm(self):
        llm_provider = os.getenv("LLM_PROVIDER")
        if llm_provider == "GOOGLE":
            return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        elif llm_provider == "OPENAI":
            return ChatOpenAI(model="gpt-4", temperature=0.7)
        elif llm_provider == "SARVAM":
            return ChatOpenAI(
                openai_api_base="https://api.sarvam.ai/v1/",
                openai_api_key=os.getenv("api_subscription_key"), # Sarvam uses OpenAI-compatible API key
                model="sarvam-m", # You might need to specify the exact model name here
                temperature=0.7
            )
        else:
            raise ValueError("LLM_PROVIDER must be 'GOOGLE', 'OPENAI', or 'SARVAM'")

    def _generate_topic_id(self, topic: str) -> str:
        """Generate consistent topic_id from topic string."""
        topic_id = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
        topic_id = re.sub(r'[\s-]+', '-', topic_id).strip('-')
        return topic_id

    def execute(self, video_script: str, topic: str):
        print("Suggesting visual assets...")
        template = """You are an expert art director. Your task is to read the provided video script and suggest appropriate visual assets (e.g., diagrams, photos, stock footage) for each section.

        Video Script:
        {video_script}

        Please provide the visual asset suggestions in JSON format, where each key is a section of the script and the value is a list of suggested visuals.
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm

        visual_assets_response = chain.invoke({"video_script": video_script})
        visual_assets_content = visual_assets_response.content
        token_usage = visual_assets_response.response_metadata.get("token_usage", {})

        # Use topic-specific directory with consistent topic_id generation
        topic_id = self._generate_topic_id(topic)
        output_dir = f"artifacts/{topic_id}"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "shotlist.json")
        
        with open(output_path, "w") as f:
            # Attempt to parse as JSON and re-dump for pretty printing
            try:
                json_content = json.loads(visual_assets_content)
                json.dump(json_content, f, indent=4)
            except json.JSONDecodeError:
                f.write(visual_assets_content) # Write as plain text if not valid JSON
        
        print(f"Visual asset suggestions generated and saved to {output_path}")
        return {"content": visual_assets_content, "token_usage": token_usage}

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.scriptwriting_agent = ScriptwritingAgent()
        self.article_writer_agent = ArticleWriterAgent()
        self.visual_asset_agent = VisualAssetAgent()

    def _generate_topic_id(self, topic: str) -> str:
        """Generate consistent topic_id from topic string."""
        import re
        # Convert to lowercase, replace spaces and special chars with hyphens
        topic_id = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
        topic_id = re.sub(r'[\s-]+', '-', topic_id).strip('-')
        return topic_id

    def execute(self, topic: str, simulate_llm_calls: bool = False):
        print(f"Orchestrating content creation for topic: {topic}")
        
        topic_id = self._generate_topic_id(topic)
        output_dir = f"artifacts/{topic_id}"
        
        # Step 1: Research
        research_content = self.research_agent.execute(topic)
        
        # Step 2: Analysis
        if simulate_llm_calls:
            print("Simulating AnalysisAgent output...")
            with open("simulated_artifacts/narrative.md", "r") as f:
                narrative_content = f.read()
            narrative_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0} # Simulated token usage
            # Write simulated narrative to topic-specific directory for test verification
            os.makedirs(output_dir, exist_ok=True)
            narrative_output_path = os.path.join(output_dir, "narrative.md")
            with open(narrative_output_path, "w") as f:
                f.write(narrative_content)
        else:
            analysis_result = self.analysis_agent.execute(research_content, topic)
            narrative_content = analysis_result["content"]
            narrative_token_usage = analysis_result["token_usage"]

        # Step 3: Scriptwriting and Article Writing (in parallel)
        if simulate_llm_calls:
            print("Simulating ScriptwritingAgent output...")
            with open("simulated_artifacts/script.md", "r") as f:
                video_script_content = f.read()
            video_script_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0} # Simulated token usage
            # Write simulated script to topic-specific directory for test verification
            os.makedirs(output_dir, exist_ok=True)
            script_output_path = os.path.join(output_dir, "script.md")
            with open(script_output_path, "w") as f:
                f.write(video_script_content)

            print("Simulating ArticleWriterAgent output...")
            with open("simulated_artifacts/article.md", "r") as f:
                web_article_content = f.read()
            web_article_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0} # Simulated token usage
            # Write simulated article to topic-specific directory for test verification
            os.makedirs(output_dir, exist_ok=True)
            article_output_path = os.path.join(output_dir, "article.md")
            with open(article_output_path, "w") as f:
                f.write(web_article_content)
        else:
            script_result = self.scriptwriting_agent.execute(narrative_content, topic)
            video_script_content = script_result["content"]
            video_script_token_usage = script_result["token_usage"]

            article_result = self.article_writer_agent.execute(narrative_content, topic)
            web_article_content = article_result["content"]
            web_article_token_usage = article_result["token_usage"]

        # Step 4: Visual Asset Suggestion
        if simulate_llm_calls:
            print("Simulating VisualAssetAgent output...")
            with open("simulated_artifacts/shotlist.json", "r") as f:
                visual_assets_content = f.read()
            visual_assets_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0} # Simulated token usage
            # Write simulated shotlist to topic-specific directory for test verification
            os.makedirs(output_dir, exist_ok=True)
            shotlist_output_path = os.path.join(output_dir, "shotlist.json")
            with open(shotlist_output_path, "w") as f:
                f.write(visual_assets_content)
        else:
            visual_assets_result = self.visual_asset_agent.execute(video_script_content, topic)
            visual_assets_content = visual_assets_result["content"]
            visual_assets_token_usage = visual_assets_result["token_usage"]
        
        total_token_usage = {
            "analysis": narrative_token_usage,
            "scriptwriting": video_script_token_usage,
            "article_writing": web_article_token_usage,
            "visual_assets": visual_assets_token_usage
        }

        print("Orchestration complete.")
        return {"video_script": video_script_content, "web_article": web_article_content, "visual_assets": visual_assets_content, "token_usage": total_token_usage}
