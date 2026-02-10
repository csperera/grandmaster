import os
from dotenv import load_dotenv
from langsmith import traceable
from src.engine.session import run_v01_session

# 1. Manually load the .env file FIRST
load_dotenv()

# 2. Wrap the session so LangSmith sees the whole "story"
@traceable(name="GrandMaster Session v0.1")
def start_demo():
    # Optional: Verify it loaded (you can remove this after it works)
    if not os.getenv("LANGCHAIN_API_KEY"):
        print("⚠️ Warning: API Key not found in environment!")
    
    run_v01_session()

if __name__ == "__main__":
    try:
        start_demo()
    except KeyboardInterrupt:
        print("\nSession ended.")
    except Exception as e:
        print(f"An error occurred: {e}")