import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

class LLMFactory:
    @staticmethod
    def get_llm(provider: str = "openai", model: str = None):
        if provider == "openai":
            return ChatOpenAI(
                model=model or "gpt-4-turbo-preview",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "google":
            return ChatGoogleGenerativeAI(
                model=model or "gemini-pro",
                google_api_key=os.getenv("GEMINI_API_KEY")
            )
        elif provider == "ollama":
            return ChatOllama(
                model=model or "llama3",
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

llm_manager = LLMFactory()
