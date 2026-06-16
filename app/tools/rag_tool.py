from app.tools.ingestion.handlers import FileIngestor, WebIngestor
from app.memory.intelligence import memory_engine
from crewai.tools import BaseTool
import os

class EnterpriseRAGTool(BaseTool):
    name: str = "enterprise_rag_tool"
    description: str = "Ingests documents or URLs and stores them in the long-term semantic memory. Input is a file path or URL."

    def _run(self, source: str) -> str:
        try:
            content = ""
            if source.startswith("http"):
                content = WebIngestor.scrape_url(source)
            elif os.path.exists(source):
                content = str(FileIngestor.read_file(source))
            else:
                return "Source not found."

            # Store in RAG memory
            memory_engine.store_experience(
                mission_id=hash(source) % 1000000,
                intent=f"Ingestion of {source}",
                result=content[:1000] # Storing a summary/snippet
            )
            return f"Successfully ingested and indexed: {source}"
        except Exception as e:
            return f"RAG Error: {str(e)}"

enterprise_rag_tool = EnterpriseRAGTool()
