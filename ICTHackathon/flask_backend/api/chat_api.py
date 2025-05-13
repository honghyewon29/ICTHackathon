import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")