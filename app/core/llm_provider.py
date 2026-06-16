import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class LLMFactory:
    @staticmethod
    def get_llm(provider: str = "openai", model: str = None):
        provider = provider.lower()
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
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model or "claude-3-opus-20240229",
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif provider == "groq":
            return ChatGroq(
                model=model or "mixtral-8x7b-32768",
                groq_api_key=os.getenv("GROQ_API_KEY")
            )
        elif provider == "deepseek":
            # DeepSeek often uses OpenAI-compatible API
            return ChatOpenAI(
                model=model or "deepseek-chat",
                openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
                openai_api_base="https://api.deepseek.com"
            )
        elif provider == "openrouter":
            return ChatOpenAI(
                model=model or "meta-llama/llama-3-70b-instruct",
                openai_api_key=os.getenv("OPENROUTER_API_KEY"),
                openai_api_base="https://openrouter.ai/api/v1"
            )
        elif provider == "ollama":
            return ChatOllama(
                model=model or "llama3",
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

llm_manager = LLMFactory()
