from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.services.vector_store import VectorStoreService
from app.config.settings import Gemini_API_KEY
from app.prompts.analyzer_prompt import FEASIBILITY_REPORT_PROMPT, JSON_FEASIBILITY_PROMPT
import json

class FeasiblityAgent:
    def __init__(self, use_gemini_embeddings: bool = False):
        print("Initializing Feasibility Agent...")
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=Gemini_API_KEY,
            model="gemini-3.5-flash",
            temperature=0.2,
        )
        print("Feasibility Agent initialized successfully.")
        self.vector_store = VectorStoreService(use_gemini=use_gemini_embeddings)
        self.prompt_template = PromptTemplate(
            template=FEASIBILITY_REPORT_PROMPT,
            input_variables=["query", "context"]
        )
        self.json_prompt_template = PromptTemplate(
            template=JSON_FEASIBILITY_PROMPT,
            input_variables=["query", "context"]
        )
        
    def analyze(self, query: str, as_json: bool = False) -> str:
        print("Fetching relevant context from the vector store...")
        similar_documents = self.vector_store.query(query, top_k=5)
        context = "\n\n".join([doc.page_content for doc in similar_documents])
        
        print("Generating feasibility report...")
        if as_json:
            prompt = self.json_prompt_template.format(query=query, context=context)
            response = self.llm.invoke(prompt)
            
            content = response.content
            if isinstance(content, list):
                content = "".join([block.get("text", "") for block in content if isinstance(block, dict)])
            elif not isinstance(content, str):
                content = str(content)
                
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            try:
                return json.loads(content.strip())
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}\nContent was: {content}")
                return {"error": "Failed to generate valid JSON"}
        else:
            prompt = self.prompt_template.format(query=query, context=context)
            response = self.llm.invoke(prompt)
            
            content = response.content
            if isinstance(content, list):
                content = "".join([block.get("text", "") for block in content if isinstance(block, dict)])
            return content
