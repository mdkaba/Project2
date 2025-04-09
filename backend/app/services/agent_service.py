# backend/app/services/agent_service.py
import asyncio
from typing import List, Dict, Optional # Added Optional

# Import Base Agent and specific agent classes
from app.agents.base import BaseAgent
from app.agents.general import GeneralAgent
from app.agents.admissions import AdmissionsAgent
from app.agents.ai_expert import AIExpertAgent
from app.core.logger import logger

class AgentService:
    """
    Service responsible for managing and routing queries to the appropriate agent.
    """
    def __init__(self):
        # Instantiate all available agents
        # In a larger application, agent loading could be dynamic or configured
        self.agents: List[BaseAgent] = [
            GeneralAgent(),
            AdmissionsAgent(),
            AIExpertAgent()
            # Add more agents here as needed
        ]
        self.agent_map: Dict[str, BaseAgent] = {agent.get_name(): agent for agent in self.agents}
        logger.info(f"AgentService initialized with agents: {[agent.get_name() for agent in self.agents]}")

    async def select_agent(self, query: str, history: list[Dict[str, str]]) -> BaseAgent:
        """
        Selects the best agent to handle the query based on confidence scores.

        Args:
            query: The user's query.
            history: The conversation history.

        Returns:
            The selected BaseAgent instance.
        """
        logger.debug(f"Selecting agent for query: '{query}'")
        if not self.agents:
            logger.error("No agents available in AgentService!")
            # Maybe return a default or raise error? Returning GeneralAgent if it exists.
            # Ensure GeneralAgent is correctly typed or handle its absence
            general_agent = self.agent_map.get("GeneralAgent")
            if general_agent:
                return general_agent
            # This case should ideally not happen if GeneralAgent is always included
            # Raising an error might be better in a production scenario
            raise ValueError("AgentService has no agents configured, cannot select agent.")

        # Get confidence scores from all agents concurrently
        # Coroutines to run: agent.should_handle(query, history)
        tasks = [agent.should_handle(query, history) for agent in self.agents]
        scores = await asyncio.gather(*tasks)

        # Find the agent with the highest score
        best_score = -1.0
        selected_agent: BaseAgent = self.agents[0] # Default to first agent initially

        for agent, score in zip(self.agents, scores):
            logger.debug(f"Agent '{agent.get_name()}' score: {score:.2f}")
            if score > best_score:
                best_score = score
                selected_agent = agent

        # Optional: Add a threshold? If no agent is confident enough, default to General?
        # threshold = 0.6
        # if best_score < threshold:
        #     logger.warning(f"No agent reached confidence threshold {threshold}. Defaulting to GeneralAgent.")
        #     selected_agent = self.agent_map.get("GeneralAgent", selected_agent) # Fallback carefully

        logger.info(f"Selected agent: '{selected_agent.get_name()}' with score {best_score:.2f}")
        return selected_agent

    def get_agent_by_name(self, name: str) -> Optional[BaseAgent]:
         """Retrieves an agent instance by its name."""
         return self.agent_map.get(name)

# Optional: Singleton instance
# agent_service = AgentService() 