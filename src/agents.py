from abc import ABC, abstractmethod
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
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
        self.web_search_tool = TavilySearchResults(max_results=5)

    def _get_llm(self):
        llm_provider = os.getenv("LLM_PROVIDER")
        if llm_provider == "GOOGLE":
            return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        elif llm_provider == "OPENAI":
            return ChatOpenAI(model="gpt-4", temperature=0.7)
        else:
            raise ValueError("LLM_PROVIDER must be 'GOOGLE' or 'OPENAI'")

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

    def execute(self, topic: str):
        print(f"Researching topic: {topic}")
        search_results = self.web_search_tool.invoke({"query": topic})
        
        urls = [result["url"] for result in search_results]
        print(f"Found URLs: {urls}")

        scraped_content_chunks = self._scrape_and_chunk(urls)
        
        sources_data = []
        for i, url in enumerate(urls):
            sources_data.append({
                "url": url,
                "content_preview": scraped_content_chunks[i][:500] if scraped_content_chunks else "No content scraped"
            })

        output_dir = "artifacts"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "sources.json")
        
        with open(output_path, "w") as f:
            json.dump(sources_data, f, indent=4)
        
        print(f"Research complete. Sources saved to {output_path}")
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
        else:
            raise ValueError("LLM_PROVIDER must be 'GOOGLE' or 'OPENAI'")

    def execute(self, research_content_chunks: list):
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
        
        narrative = chain.invoke({"research_content": summarized_content})

        output_dir = "artifacts"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "narrative.md")
        
        with open(output_path, "w") as f:
            f.write(narrative.content)
        
        print(f"Analysis complete. Narrative saved to {output_path}")
        return narrative.content

    def _summarize_chunks(self, chunks: list):
        print("Summarizing research chunks...")
        summaries = []
        summary_template = """Please provide a concise summary of the following text:

{text}

Summary:"""
        summary_prompt = ChatPromptTemplate.from_template(summary_template)
        summary_chain = summary_prompt | self.llm

        # Limit the number of chunks to process to avoid rate limits
        max_chunks_to_process = 50  # Adjust this value as needed
        for i, chunk in enumerate(chunks[:max_chunks_to_process]):
            try:
                summary = summary_chain.invoke({"text": chunk})
                summaries.append(summary.content)
                print(f"Summarized chunk {i+1}/{len(chunks)}")
            except Exception as e:
                print(f"Error summarizing chunk {i+1}: {e}")
                summaries.append("Error summarizing chunk.") # Add a placeholder for failed summaries
        
        return "\n\n".join(summaries)
