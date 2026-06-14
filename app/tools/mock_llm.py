from typing import Any, List, Optional
from langchain.llms.base import LLM
from pydantic import Field

class MockLLM(LLM):
    """A mock LLM for testing and local simulation."""

    model_name: str = Field(default="mock-model")

    @property
    def _llm_type(self) -> str:
        return "mock"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        """Mock call that returns a generic response based on the prompt."""
        if "CEO" in prompt:
            return "As the Friday CEO, I have analyzed the requirements and delegated tasks to the team."
        elif "Scout" in prompt:
            return "Found 5 new freelance leads on Upwork and Freelancer. Generated proposals for each."
        elif "QA" in prompt:
            return "Audit complete. No major issues found. Data integrity verified."
        elif "Clean" in prompt:
            return "Data cleaning complete. Removed 150 null values and 20 duplicates."
        else:
            return f"Mock response for: {prompt[:50]}..."

    @property
    def _identifying_params(self) -> dict:
        return {"model_name": self.model_name}
