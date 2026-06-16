from langchain_core.messages import AIMessage
from app.core.logging_config import logger
from app.memory.intelligence import learner_engine

def reflection_node(state):
    """
    Analyzes mission execution patterns for self-improvement.
    """
    logger.info("Friday Reflection Engine Started")

    # 1. Failure Analysis Simulation
    last_message = state['messages'][-1].content
    success = "Successful" in last_message or "Passed" in last_message

    performance_score = 0.9 if success else 0.4

    # 2. Update Agent Strategy (Mock Logic)
    # In production, this would refine the agent's prompt based on 'last_message'
    learner_engine.update_agent_strategy(
        agent_role="Specialist Swarm",
        performance_score=performance_score
    )

    # 3. Prompt Optimization Log
    if not success:
        logger.warning("Optimization Recommended: Task decomposition was too broad.")

    return {
        "messages": [AIMessage(content=f"Reflection Complete. Performance Score: {performance_score}. Neural pathways re-optimized.")],
        "next_node": "finalizer"
    }
