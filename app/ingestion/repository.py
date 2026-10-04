import os
from pathlib import Path
from typing import List, Dict, Any

class LocalRepositoryLoader:
    """
    Loads source code files from a local directory path.
    """
    def __init__(self, root_path: str, supported_extensions: List[str] = None):
        self.root_path = Path(root_path)
        if not self.root_path.exists() or not self.root_path.is_dir():
            raise ValueError(f"The path {root_path} does not exist or is not a directory.")
        
        # Expanded list of common programming languages and Teamcenter specific files
        self.supported_extensions = supported_extensions or [
            # Teamcenter specific
            ".c", ".cpp", ".h", ".hpp", ".cxx", ".hxx", # ITK (C/C++)
            ".java",                                    # RAC (Java)
            ".js", ".ts", ".jsx", ".tsx", ".html", ".css", # Active Workspace / Web
            ".xml",                                     # BMIDE
            
            # Additional common languages
            ".py", ".pyw",                              # Python
            ".cs",                                      # C#
            ".go",                                      # Go
            ".rs",                                      # Rust
            ".rb",                                      # Ruby
            ".php",                                     # PHP
            ".sh", ".bash", ".bat", ".ps1",             # Shell / Scripts
            ".sql",                                     # Database
            
            # Configs and Documentation
            ".json", ".yaml", ".yml", ".toml", ".ini",  # Configs
            ".md", ".txt"                               # Documentation
        ]

    def load_files(self) -> List[Dict[str, Any]]:
        """
        Recursively walks the directory and yields file content and metadata.
        """
        documents = []
        for dirpath, _, filenames in os.walk(self.root_path):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                
                if file_path.suffix.lower() in self.supported_extensions:
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        # Extract metadata
                        relative_path = file_path.relative_to(self.root_path)
                        metadata = {
                            "source": str(file_path),
                            "relative_path": str(relative_path),
                            "filename": filename,
                            "extension": file_path.suffix.lower()
                        }
                        
                        documents.append({
                            "content": content,
                            "metadata": metadata
                        })
                    except Exception as e:
                        print(f"Failed to read {file_path}: {e}")
                        
        return documents

import subprocess
import tempfile
import shutil

class GithubRepositoryLoaderWrapper:
    """
    Loads source code files directly from a GitHub repository by temporarily cloning it.
    This avoids GitHub API rate limits and is much faster.
    """
    def __init__(self, repo_url: str, branch: str = "main", supported_extensions: List[str] = None):
        self.repo_url = repo_url
        self.branch = branch
        
        self.supported_extensions = supported_extensions or [
            ".c", ".cpp", ".h", ".hpp", ".cxx", ".hxx",
            ".java", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".xml",
            ".py", ".pyw", ".cs", ".go", ".rs", ".rb", ".php",
            ".sh", ".bash", ".bat", ".ps1", ".sql",
            ".json", ".yaml", ".yml", ".toml", ".ini", ".md", ".txt"
        ]

    def load_files(self) -> List[Dict[str, Any]]:
        """
        Clones the repo to a temporary directory, loads the files using LocalRepositoryLoader, 
        and then deletes the temporary directory.
        """
        documents = []
        temp_dir = tempfile.mkdtemp()
        
        print(f"Cloning {self.repo_url} (Branch: {self.branch}) into temporary storage...")
        try:
            # Clone the repo deeply (depth 1 for speed), letting git auto-detect the default branch
            subprocess.run(
                ["git", "clone", "--depth", "1", self.repo_url, temp_dir],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            
            # Use our existing Local Loader on the cloned files
            local_loader = LocalRepositoryLoader(root_path=temp_dir, supported_extensions=self.supported_extensions)
            raw_docs = local_loader.load_files()
            
            # Update the metadata to point to the GitHub URL instead of the temp folder
            for doc in raw_docs:
                relative_path = doc["metadata"]["relative_path"]
                # Convert Windows slashes to URL slashes
                url_path = relative_path.replace("\\", "/")
                
                doc["metadata"]["source"] = f"{self.repo_url}/blob/{self.branch}/{url_path}"
                documents.append(doc)
                
            print(f"Successfully loaded {len(documents)} files from GitHub.")
            
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e.stderr.decode('utf-8')}")
        finally:
            # Clean up the temporary directory
            print("Cleaning up temporary repository files...")
            # On Windows, shutil.rmtree sometimes fails on .git folders, so we ignore errors
            shutil.rmtree(temp_dir, ignore_errors=True)
            
        return documents
