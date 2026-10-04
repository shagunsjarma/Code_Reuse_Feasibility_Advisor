import os
import sys
# Ensure Python can find the 'app' module when running this script directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.ingestion.repository import LocalRepositoryLoader, GithubRepositoryLoaderWrapper
from app.ingestion.chunker import CodeChunker
from app.services.vector_store import VectorStoreService

class CodeIndexer:
    def __init__(self, use_gemini_embeddings: bool = False):
        """
        Initializes the indexing pipeline.
        """
        self.chunker = CodeChunker(chunk_size=1500, chunk_overlap=200)
        self.vector_store = VectorStoreService(use_gemini=use_gemini_embeddings)

    def index_repository(self, path_or_url: str):
        """
        The main pipeline: Load -> Chunk -> Embed & Store
        """
        print(f"\n--- Starting ingestion for: {path_or_url} ---")
        
        # 1. Load the files (Dynamically choose Local or Github)
        print("1. Loading files...")
        
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            loader = GithubRepositoryLoaderWrapper(repo_url=path_or_url)
        else:
            if not os.path.exists(path_or_url):
                print(f"Error: Local directory '{path_or_url}' does not exist.")
                return
            loader = LocalRepositoryLoader(root_path=path_or_url)
            
        raw_documents = loader.load_files()
        
        if not raw_documents:
            print("No supported code files found.")
            return

        # 2. Chunk the files
        print(f"2. Chunking {len(raw_documents)} files...")
        chunks = self.chunker.chunk_documents(raw_documents)
        print(f"   Created {len(chunks)} chunks.")

        # 3. Store in the Vector Database
        print("3. Generating embeddings and saving to ChromaDB...")
        self.vector_store.add_documents(chunks)
        
        print("Success! Indexing Complete! Your codebase is now ready for AI analysis.\n")

if __name__ == "__main__":
    import sys
    
    repo_input = ""
    if len(sys.argv) > 1:
        repo_input = sys.argv[1]
    else:
        repo_input = input("Enter the absolute path OR the GitHub URL of the repository to index: ")
    
    if repo_input.strip():
        # We use local HuggingFace embeddings by default to save API costs
        indexer = CodeIndexer(use_gemini_embeddings=False) 
        indexer.index_repository(repo_input.strip())
    else:
        print("Error: Invalid input.")
