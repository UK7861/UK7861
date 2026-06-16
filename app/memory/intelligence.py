import chromadb
from sentence_transformers import SentenceTransformer
from app.memory.graph import graph_memory
from app.db.redis_bus import redis_cache
from app.core.logging_config import logger
import os

# Initialize Vector DB
chroma_client = chromadb.PersistentClient(path="app/vault/chroma_db")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class LongTermMemory:
    def __init__(self):
        self.collection = chroma_client.get_or_create_collection(name="mission_memory")

    def store_experience(self, mission_id: int, intent: str, result: str):
        # 1. Semantic Memory (ChromaDB)
        embedding = embedding_model.encode(intent).tolist()
        self.collection.add(
            embeddings=[embedding],
            documents=[intent],
            metadatas=[{"mission_id": mission_id, "result": result}],
            ids=[str(mission_id)]
        )

        # 2. Knowledge Graph Memory (Neo4j)
        graph_memory.add_knowledge("Mission", f"COMPLETED_{mission_id}", intent)

        # 3. Episodic Memory (Redis)
        redis_cache.set_state(f"mission:{mission_id}:result", result)
        logger.info("Experience Stored", mission_id=mission_id)

    def retrieve_context(self, query: str):
        # 1. Semantic Search
        query_embedding = embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        # 2. Graph Context
        graph_context = graph_memory.get_graph()

        return {
            "semantic_memory": results['documents'],
            "graph_memory": graph_context
        }

class AgentLearner:
    @staticmethod
    def update_agent_strategy(agent_role: str, performance_score: float):
        # Logic to evolve agent prompts or tools based on mission success
        logger.info("Agent Learning Strategy Updated", role=agent_role, score=performance_score)
        # Increment global intel level in Redis
        current_intel = int(redis_cache.get_state("intel_level") or 1000)
        redis_cache.set_state("intel_level", str(current_intel + int(performance_score * 10)))

memory_engine = LongTermMemory()
learner_engine = AgentLearner()
