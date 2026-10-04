from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config.settings import HF_TOKEN, Gemini_API_KEY

class EmbeddingsService:
    def __init__(self, use_gemini: bool = False):
        self.use_gemini = use_gemini
        if self.use_gemini:
            # Fixed the class name and the model name
            self.model = GoogleGenerativeAIEmbeddings(google_api_key=Gemini_API_KEY, model="models/gemini-embedding-2")
        else:
            # Removed the invalid huggingfacehub_api_token argument (it runs locally so it doesn't need it)
            self.model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})
            
    def get_model(self):
        """
        Returns the embedding model object itself.
        This is required for LangChain Vector Stores (like Chroma).
        """
        return self.model

    def get_embeddings(self, texts: list) -> list:
        """
        Generate embeddings for a list of texts directly.
        """
        return self.model.embed_documents(texts)
