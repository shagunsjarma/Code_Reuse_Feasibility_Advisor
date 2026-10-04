# Code Reuse Feasibility Analyzer 🚀

The **Code Reuse Feasibility Analyzer** is an Enterprise Engineering Intelligence tool powered by Retrieval-Augmented Generation (RAG). It allows software architects and frontend/backend developers to instantly query their local codebases or GitHub repositories to find reusable components before building from scratch.

By leveraging **ChromaDB** for vector storage, **HuggingFace** for local embeddings, and **Google Gemini 3.5 Flash** for advanced reasoning, the system generates comprehensive Feasibility Reports structured as actionable insights.

## ✨ Features

*   **GitHub & Local Ingestion:** Seamlessly index both local project directories and remote GitHub repositories. Uses an optimized local Git cloning method to bypass GitHub API rate limits.
*   **Semantic Code Search:** Uses `all-MiniLM-L6-v2` embeddings via HuggingFace to semantically understand code chunks (classes, methods, components).
*   **AI Feasibility Reports:** Gemini analyzes the retrieved code context against your requested feature and determines a "Reuse Confidence" score.
*   **Two Interfaces:** 
    *   **Gorgeous Web Dashboard:** A highly-polished FastAPI-powered web interface offering detailed metrics, risk summaries, and interactive pipeline steps.
    *   **Terminal CLI:** A classic text-based interactive loop for terminal power users.
*   **Structured JSON AI Output:** The LLM is strictly constrained to output structured JSON data to directly populate the web dashboard metrics.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3, FastAPI, Uvicorn
*   **AI/RAG:** LangChain, Google GenAI (Gemini 3.5 Flash), ChromaDB, HuggingFace (`sentence-transformers`)
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS, No-build)

---

## 🚀 Getting Started

### 1. Prerequisites
*   Python 3.10+
*   Git installed on your system
*   A Google Gemini API Key

### 2. Installation
Clone the repository and set up your virtual environment:

```bash
# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # On Windows
# source .venv/bin/activate # On Mac/Linux

# Install all required dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your Gemini API Key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## 💻 Usage

### Indexing a Repository
Before searching, you need to ingest a codebase (so it can be stored in the local ChromaDB database).

```bash
# Index a remote GitHub repository
python app/ingestion/indexer.py https://github.com/reactjs/react-tutorial

# Or index a local directory
python app/ingestion/indexer.py C:/Projects/my-local-app
```

### Running the Web Dashboard (Recommended)
Start the FastAPI server to access the visual dashboard:

```bash
python app/api/api.py
```
*Open your browser and navigate to **`http://localhost:8000`**.*

### Running the CLI Interface
If you prefer the terminal, you can interact with the agent via the CLI loop:

```bash
python app/main.py
```

---

## 📁 Project Structure

```text
Code_Reuse_feasibility_report/
│
├── app/
│   ├── agents/
│   │   └── analyzer_agent_.py      # Gemini LLM Langchain wrapper & logic
│   ├── api/
│   │   └── api.py                  # FastAPI Web Server & UI endpoints
│   ├── config/
│   │   └── settings.py             # Environment variables loading
│   ├── ingestion/
│   │   ├── indexer.py              # Main orchestrator for chunking/saving
│   │   └── repository.py           # Local file loader & Github Cloner
│   ├── prompts/
│   │   └── analyzer_prompt.py      # LLM instructions (Text & JSON schemas)
│   ├── services/
│   │   ├── embeddings.py           # HuggingFace Embeddings wrapper
│   │   └── vector_store.py         # ChromaDB management
│   └── main.py                     # Interactive Terminal CLI loop
│
├── vector_store/                   # Local Chroma SQLite Database (auto-generated)
├── index.html                      # The stunning Frontend Web UI
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## ⚠️ Notes
*   **Large Repositories:** Indexing massive repositories (like the main `facebook/react` repo) can take several minutes to embed locally on a CPU. Start with smaller test repositories.
*   **LangChain Warnings:** You may see a warning about "Direct use of automatic function calling (AFC)". This is normal behavior for the current `gemini-3.5-flash` LangChain integration and does not affect the output.
