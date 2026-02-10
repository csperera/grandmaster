import os
from dotenv import load_dotenv, find_dotenv

print(f"Looking for .env at: {find_dotenv()}")
load_dotenv(find_dotenv())

print(f"LangChain Key Found: {'✅' if os.getenv('LANGCHAIN_API_KEY') else '❌'}")
print(f"OpenAI Key Found:    {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")