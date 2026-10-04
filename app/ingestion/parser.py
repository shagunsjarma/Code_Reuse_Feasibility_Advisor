import ast
from pathlib import Path
from typing import Any, Dict, List
import javalang
import pyjsparser


def python_ast_to_dict(node):
    """Helper to convert Python AST to dictionary"""
    if isinstance(node, ast.AST):
        result = {"_type": type(node).__name__}
        for field in node._fields:
            if hasattr(node, field):
                result[field] = python_ast_to_dict(getattr(node, field))
        return result
    elif isinstance(node, list):
        return [python_ast_to_dict(item) for item in node]
    else:
        return node

def java_ast_to_dict(node):
    """Helper to convert Java AST to dictionary"""
    if isinstance(node, javalang.tree.Node):
        result = {"_type": type(node).__name__}
        if hasattr(node, 'attrs'):
            for attr in node.attrs:
                result[attr] = java_ast_to_dict(getattr(node, attr, None))
        return result
    elif isinstance(node, (list, tuple, set)):
        return [java_ast_to_dict(item) for item in node]
    else:
        return node


class CodeParser:
    def __init__(self, supported_extensions: List[str] = None):
        self.supported_extensions = supported_extensions or [
            ".py", ".java", ".js", ".ts", ".cpp", ".c", ".h", ".hpp", ".cs"
        ]
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a code file and return its abstract syntax tree (AST) representation.
        
        Args:
            file_path (str): The path to the code file.
        returns:
            Dict[str, Any]: A dictionary containing the AST representation of the code.
        """
        file_extension = Path(file_path).suffix
        if file_extension not in self.supported_extensions:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
            if file_extension == ".py":
                return self._parse_python_code(code)
            elif file_extension == ".java":
                return self._parse_java_code(code)
            elif file_extension in [".js", ".ts"]:
                return self._parse_javascript_code(code)
            elif file_extension in [".cpp", ".c", ".h", ".hpp"]:
                return self._parse_cpp_code(code)
            elif file_extension == ".cs":
                return self._parse_csharp_code(code)
            else:
                raise ValueError(f"Unsupported file extension: {file_extension}")
    
    def _parse_python_code(self, code: str) -> Dict[str, Any]:
        """Parse Python code and return its AST representation."""
        try:
            tree = ast.parse(code)
            return python_ast_to_dict(tree)
        except Exception as e:
            raise ValueError(f"Error parsing Python code: {e}")
        
    def _parse_java_code(self, code: str) -> Dict[str, Any]:
        """Parse Java code and return its AST representation."""
        try:
            tree = javalang.parse.parse(code)
            return java_ast_to_dict(tree)
        except Exception as e:
            raise ValueError(f"Error parsing Java code: {e}")
    
    def _parse_javascript_code(self, code: str) -> Dict[str, Any]:
        """Parse JavaScript code and return its AST representation."""
        try:
            tree = pyjsparser.parse(code)
            # pyjsparser already returns a dictionary, no helper needed!
            return tree
        except Exception as e:
            raise ValueError(f"Error parsing JavaScript/TypeScript code: {e}")
        
    def _parse_cpp_code(self, code: str) -> Dict[str, Any]:
        """Parse C/C++ code. Returns basic info for now to prevent crashes."""
        return {"_type": "cpp_source", "content_length": len(code), "message": "C/C++ full AST parsing not implemented."}
    
    def _parse_csharp_code(self, code: str) -> Dict[str, Any]:
        """Parse C# code. Returns basic info for now to prevent crashes."""
        return {"_type": "csharp_source", "content_length": len(code), "message": "C# full AST parsing not implemented."}
    
    def parse_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        Parse all code files in a directory and return their AST representations.
        """
        ast_representations = {}
        for file_path in Path(directory_path).rglob('*'):
            if file_path.is_file() and file_path.suffix in self.supported_extensions:
                try:
                    ast_representations[str(file_path)] = self.parse_file(str(file_path))
                except Exception as e:
                    ast_representations[str(file_path)] = {"error": str(e)}
        return ast_representations