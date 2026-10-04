from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

class CodeChunker:
    """
    Chunks source code files into smaller, semantically meaningful pieces
    using LangChain's language-aware recursive text splitter.
    """
    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Map file extensions to LangChain Language enums
        self.extension_to_language = {
            ".py": Language.PYTHON,
            ".java": Language.JAVA,
            ".js": Language.JS,
            ".ts": Language.TS,
            ".cpp": Language.CPP,
            ".c": Language.CPP,
            ".h": Language.CPP,
            ".hpp": Language.CPP,
            ".cs": Language.CSHARP,
            ".html": Language.HTML,
            ".rb": Language.RUBY,
            ".rs": Language.RUST,
            ".go": Language.GO,
            ".php": Language.PHP
        }

    def get_splitter_for_extension(self, extension: str) -> RecursiveCharacterTextSplitter:
        """Returns the appropriate text splitter for a given file extension."""
        ext_lower = extension.lower()
        if ext_lower in self.extension_to_language:
            lang = self.extension_to_language[ext_lower]
            return RecursiveCharacterTextSplitter.from_language(
                language=lang,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
        else:
            # Fallback to standard text splitting for unknown or generic files (e.g. XML, JSON, txt)
            return RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of document dictionaries (from repository.py) and chunks them.
        Returns a flat list of chunk dictionaries, preserving and enriching metadata.
        """
        all_chunks = []
        
        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            extension = metadata.get("extension", "")
            
            if not content.strip():
                continue
                
            splitter = self.get_splitter_for_extension(extension)
            
            # Split the text
            chunks = splitter.split_text(content)
            
            # Re-package into our dictionary format with updated metadata
            for i, chunk_text in enumerate(chunks):
                chunk_metadata = metadata.copy()
                chunk_metadata["chunk_index"] = i
                chunk_metadata["chunk_size"] = len(chunk_text)
                
                all_chunks.append({
                    "content": chunk_text,
                    "metadata": chunk_metadata
                })
                
        return all_chunks

# Example Usage
if __name__ == "__main__":
    # Mock document structure matching what repository.py produces
    sample_docs = [
        {
            "content": "class MyClass:\n    def method_one(self):\n        pass\n\n    def method_two(self):\n        print('hello')\n",
            "metadata": {"filename": "test.py", "extension": ".py"}
        }
    ]
    # Intentionally small chunk size for testing demonstration
    chunker = CodeChunker(chunk_size=50, chunk_overlap=10)
    chunks = chunker.chunk_documents(sample_docs)
    for c in chunks:
        print(f"--- Chunk {c['metadata']['chunk_index']} ---")
        print(c["content"])
