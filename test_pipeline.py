import json
from app.ingestion.repository import LocalRepositoryLoader
from app.ingestion.parser import CodeParser
from app.ingestion.chunker import CodeChunker

def run_test():
    print("=== 1. Testing LocalRepositoryLoader ===")
    loader = LocalRepositoryLoader("test_data")
    docs = loader.load_files()
    print(f"Loaded {len(docs)} files.")
    for d in docs:
        print(f" - Found file: {d['metadata']['filename']} ({d['metadata']['extension']})")

    print("\n=== 2. Testing CodeChunker ===")
    # Using a smaller chunk size for testing to force it to split the code
    chunker = CodeChunker(chunk_size=100, chunk_overlap=20)
    chunks = chunker.chunk_documents(docs)
    print(f"Generated {len(chunks)} chunks.")
    
    # Print the first two chunks to verify
    for i in range(min(2, len(chunks))):
        print(f"\nChunk {i} (from {chunks[i]['metadata']['filename']}):")
        print("-" * 20)
        print(chunks[i]['content'])
        print("-" * 20)

    print("\n=== 3. Testing CodeParser (AST Extraction) ===")
    parser = CodeParser()
    ast_results = parser.parse_directory("test_data")
    print(f"Successfully extracted ASTs for {len(ast_results)} files.")
    
    # Print a tiny snippet of the AST for the python file
    for filepath, ast_tree in ast_results.items():
        if "sample.py" in filepath:
            print(f"\nAST structure for sample.py:")
            # Just print the first 200 characters of the AST dictionary string
            print(str(ast_tree)[:300] + "...")
            break

if __name__ == "__main__":
    run_test()
