import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "friday_neo4j_password")

class Neo4jMemory:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def add_knowledge(self, entity_a: str, relation: str, entity_b: str):
        with self.driver.session() as session:
            session.execute_write(self._create_relation, entity_a, relation, entity_b)

    @staticmethod
    def _create_relation(tx, a, rel, b):
        query = (
            "MERGE (node_a:Entity {name: $a}) "
            "MERGE (node_b:Entity {name: $b}) "
            f"MERGE (node_a)-[r:{rel.upper()}]->(node_b) "
            "RETURN r"
        )
        tx.run(query, a=a, b=b)

    def get_graph(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n)-[r]->(m) RETURN n.name as source, type(r) as relation, m.name as target LIMIT 100")
            nodes = set()
            links = []
            for record in result:
                nodes.add(record["source"])
                nodes.add(record["target"])
                links.append({"source": record["source"], "target": record["target"], "type": record["relation"]})

            return {
                "nodes": [{"id": name} for name in nodes],
                "links": links
            }

graph_memory = Neo4jMemory()
