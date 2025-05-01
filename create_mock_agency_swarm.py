#!/usr/bin/env python3
"""
Create Mock Agency-Swarm Package
-------------------------------
This script creates a mock implementation of the agency-swarm package,
which allows the Instagram Automation Tool to run without the actual
agency-swarm package installed.
"""

import os
import sys
import shutil

def create_mock_agency_swarm():
    """Create a mock implementation of the agency-swarm package."""
    print("Creating mock implementation of agency-swarm...")
    
    mock_dir = "mock_agency_swarm"
    
    # Remove existing directory if it exists
    if os.path.exists(mock_dir):
        print(f"Removing existing {mock_dir} directory...")
        shutil.rmtree(mock_dir)
    
    # Create directory
    print(f"Creating {mock_dir} directory...")
    os.makedirs(mock_dir, exist_ok=True)
    
    # Create __init__.py
    with open(os.path.join(mock_dir, "__init__.py"), "w") as f:
        f.write("""\"\"\"
Mock implementation of the agency-swarm package.
\"\"\"

from .agency import Agency
from .agent import Agent
from .task import Task

__all__ = ['Agency', 'Agent', 'Task']
""")
    
    # Create agency.py
    with open(os.path.join(mock_dir, "agency.py"), "w") as f:
        f.write("""\"\"\"
Mock implementation of the Agency class.
\"\"\"

import logging

logger = logging.getLogger(__name__)

class Agency:
    \"\"\"Mock Agency class for demonstration purposes.\"\"\"
    
    def __init__(self, name=None, description=None, agents=None):
        \"\"\"Initialize the Agency.\"\"\"
        self.name = name
        self.description = description
        self.agents = agents or []
        self.agent_map = {agent.name: agent for agent in self.agents}
        
        # Set agency reference for each agent
        for agent in self.agents:
            agent.agency = self
        
        logger.info(f"Agency '{name}' initialized with {len(self.agents)} agents")
    
    def add_communication(self, agent1, agent2):
        \"\"\"Add communication between agents.\"\"\"
        logger.info(f"Added communication between {agent1.name} and {agent2.name}")
    
    def get_agent(self, agent_name):
        \"\"\"Get an agent by name.\"\"\"
        agent = self.agent_map.get(agent_name)
        if not agent:
            logger.warning(f"Agent '{agent_name}' not found")
        return agent
""")
    
    # Create agent.py
    with open(os.path.join(mock_dir, "agent.py"), "w") as f:
        f.write("""\"\"\"
Mock implementation of the Agent class.
\"\"\"

import logging

logger = logging.getLogger(__name__)

class Agent:
    \"\"\"Mock Agent class for demonstration purposes.\"\"\"
    
    def __init__(self, name=None, description=None, instructions=None):
        \"\"\"Initialize the Agent.\"\"\"
        self.name = name
        self.description = description
        self.instructions = instructions
        self.agency = None
        
        logger.info(f"Agent '{name}' initialized")
    
    def __str__(self):
        return f"Agent({self.name})"
    
    def __repr__(self):
        return self.__str__()
""")
    
    # Create task.py
    with open(os.path.join(mock_dir, "task.py"), "w") as f:
        f.write("""\"\"\"
Mock implementation of the Task decorator.
\"\"\"

import logging
import functools

logger = logging.getLogger(__name__)

def Task(func):
    \"\"\"Mock Task decorator for demonstration purposes.\"\"\"
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing task: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
""")
    
    # Create setup.py
    with open(os.path.join(mock_dir, "setup.py"), "w") as f:
        f.write("""
from setuptools import setup, find_packages

setup(
    name="agency-swarm",
    version="0.1.0",
    packages=find_packages(),
    description="Mock implementation of agency-swarm for Instagram Automation Tool",
    author="Your Name",
    author_email="your.email@example.com",
)
""")
    
    print(f"Mock implementation created in {mock_dir}")
    print(f"To install, run: pip install -e {mock_dir}")
    
    # Automatically install without asking
    import subprocess
    print(f"Installing mock agency-swarm...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", mock_dir])
        print("Mock agency-swarm installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing mock agency-swarm: {e}")
        print("You can manually install it with: pip install -e mock_agency_swarm")
    except Exception as e:
        print(f"Unexpected error installing mock agency-swarm: {e}")
        print("You can manually install it with: pip install -e mock_agency_swarm")

if __name__ == "__main__":
    try:
        create_mock_agency_swarm()
        print("Mock agency-swarm creation completed.")
    except Exception as e:
        print(f"Error creating mock agency-swarm: {e}")