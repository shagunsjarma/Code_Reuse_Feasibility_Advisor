from langchain_chroma import Chroma
from app.services.embeddings import EmbeddingsService
from langchain_core.documents import Document


class VectorStoreService:
    def __init__(self, persist_directory: str = "vector_store", use_gemini: bool = False):
        self.persist_directory = persist_directory
        self.embeddings_service = EmbeddingsService(use_gemini = use_gemini)
        self.vector_store = Chroma(
            collection_name="code_reuse_collection",
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings_service.get_model()
        )
    
    def add_documents(self, chunks : list):
        """
        Add a list of documents to the vector store.
        
        Args:
            documents (list): A list of Document objects to be added to the vector store.
        """
        doc = []
        for chunk in chunks:
            doc.append(Document(page_content=chunk['content'], metadata=chunk['metadata']))
        self.vector_store.add_documents(doc)
        
        
    
    def query(self, query_text: str, top_k: int = 5) -> list:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text (str): The text to query the vector store.
            top_k (int): The number of top similar documents to retrieve.
        returns:
            list: A list of Document objects that are most similar to the query text.
        """
        # Chroma's similarity_search automatically embeds the text for you!
        results = self.vector_store.similarity_search(query_text, k=top_k)
        return results
    
