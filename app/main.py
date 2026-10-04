import sys
import os

# Ensure Python can find your 'app' folder when running from the command line
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.analyzer_agent_ import FeasiblityAgent

def main():
    print("="*60)
    print("🚀 Welcome to the Code Reuse Feasibility Analyzer! 🚀")
    print("="*60)
    
    # Initialize your agent (using local HuggingFace embeddings by default)
    try:
        agent = FeasiblityAgent(use_gemini_embeddings=False)
    except Exception as e:
        print(f"❌ Failed to initialize the Agent: {e}")
        print("Please ensure your .env file has the GOOGLE_API_KEY set.")
        return
    
    while True:
        print("\n" + "-"*60)
        question = input("What feature do you want to build or reuse? (or 'quit' to exit):\n> ")
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
            
        if not question.strip():
            continue
            
        print("\n🧠 Thinking... Searching codebase and writing report...\n")
        
        try:
            report = agent.analyze(question)
            print("\n" + "="*20 + " FEASIBILITY REPORT " + "="*20)
            print(report)
            print("="*60)
        except Exception as e:
            print(f"\n❌ An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()
