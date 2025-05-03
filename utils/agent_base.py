"""
Agent Base Module
----------------
Base classes for agents and tasks in the Instagram Automation Tool.
This module resolves circular imports between the main tool and agent modules.
"""

import logging
import functools
from typing import Any, Callable, Dict, List, Optional, TypeVar

logger = logging.getLogger(__name__)

# Type for decorated function
F = TypeVar('F', bound=Callable[..., Any])

class Agency:
    """Base Agency class for managing agents."""
    
    def __init__(self, name: str = None, description: str = None, agents: List[Any] = None):
        """Initialize the Agency.
        
        Args:
            name: Name of the agency
            description: Description of the agency
            agents: List of agents in the agency
        """
        self.name = name
        self.description = description
        self.agents = agents or []
        self.agent_map = {agent.name: agent for agent in self.agents}
        
        # Set agency reference for each agent
        for agent in self.agents:
            agent.agency = self
        
        logger.info(f"Agency '{name}' initialized with {len(self.agents)} agents")
    
    def add_communication(self, agent1: Any, agent2: Any) -> None:
        """Add communication between agents.
        
        Args:
            agent1: First agent
            agent2: Second agent
        """
        logger.info(f"Added communication between {agent1.name} and {agent2.name}")
    
    def get_agent(self, agent_name: str) -> Optional[Any]:
        """Get an agent by name.
        
        Args:
            agent_name: Name of the agent to get
            
        Returns:
            Agent if found, None otherwise
        """
        agent = self.agent_map.get(agent_name)
        if not agent:
            logger.warning(f"Agent '{agent_name}' not found")
        return agent

class Agent:
    """Base Agent class for all agents in the system."""
    
    def __init__(self, name: str = None, description: str = None, instructions: str = None):
        """Initialize the Agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent
            instructions: Instructions for the agent
        """
        self.name = name
        self.description = description
        self.instructions = instructions
        self.agency = None
        
        logger.info(f"Agent '{name}' initialized")
    
    def __str__(self) -> str:
        return f"Agent({self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()

def Task(func: F) -> F:
    """Decorator for agent tasks.
    
    This decorator logs when a task is executed and provides
    a common way to identify task methods in agent classes.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing task: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper