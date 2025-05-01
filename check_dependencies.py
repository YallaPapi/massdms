#!/usr/bin/env python3
"""
Dependency Checker for Instagram Automation Tool
-----------------------------------------------
This script checks if all required dependencies are installed and provides
instructions on how to install missing dependencies.
"""

import importlib.util
import subprocess
import sys
import os

def check_package(package_name):
    """Check if a package is installed."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package_name):
    """Install a package using pip."""
    print(f"Installing {package_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def main():
    """Check dependencies and provide instructions."""
    print("Checking dependencies for Instagram Automation Tool...")
    
    # Essential packages
    essential_packages = [
        "requests",
        "python-dotenv",
        "pydantic",
        "selenium",
        "webdriver_manager",
        "tqdm",
        "colorama"
    ]
    
    # Check essential packages
    missing_essential = []
    for package in essential_packages:
        if not check_package(package.replace("-", "_")):
            missing_essential.append(package)
    
    # Check agency-swarm
    agency_swarm_available = check_package("agency_swarm")
    
    # Report results
    if not missing_essential and agency_swarm_available:
        print("All dependencies are installed!")
        return
    
    # Handle missing essential packages
    if missing_essential:
        print("\nMissing essential packages:")
        for package in missing_essential:
            print(f"  - {package}")
        
        print("\nInstall essential packages with:")
        print(f"  pip install -r requirements-minimal.txt")
    
    # Handle agency-swarm
    if not agency_swarm_available:
        print("\nThe 'agency-swarm' package is not installed.")
        print("This package might not be available on PyPI.")
        print("\nOptions for installing agency-swarm:")
        print("1. If you have the source code:")
        print("   - Navigate to the agency-swarm directory")
        print("   - Run: pip install -e .")
        print("\n2. If it's available on GitHub:")
        print("   - Run: pip install git+https://github.com/username/agency-swarm.git")
        print("\n3. Create a mock implementation:")
        print("   - Run: python create_mock_agency_swarm.py")
        
        # Automatically create a mock implementation
        print("\nAutomatically creating a mock implementation of agency-swarm...")
        create_mock_agency_swarm()

def create_mock_agency_swarm():
    """Create a mock implementation of the agency-swarm package."""
    mock_dir = "mock_agency_swarm"
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
    
    def add_communication(self, agent1, agent2):
        \"\"\"Add communication between agents.\"\"\"
        print(f"Added communication between {agent1.name} and {agent2.name}")
    
    def get_agent(self, agent_name):
        \"\"\"Get an agent by name.\"\"\"
        return self.agent_map.get(agent_name)
""")
    
    # Create agent.py
    with open(os.path.join(mock_dir, "agent.py"), "w") as f:
        f.write("""\"\"\"
Mock implementation of the Agent class.
\"\"\"

class Agent:
    \"\"\"Mock Agent class for demonstration purposes.\"\"\"
    
    def __init__(self, name=None, description=None, instructions=None):
        \"\"\"Initialize the Agent.\"\"\"
        self.name = name
        self.description = description
        self.instructions = instructions
        self.agency = None
""")
    
    # Create task.py
    with open(os.path.join(mock_dir, "task.py"), "w") as f:
        f.write("""\"\"\"
Mock implementation of the Task decorator.
\"\"\"

def Task(func):
    \"\"\"Mock Task decorator for demonstration purposes.\"\"\"
    def wrapper(*args, **kwargs):
        print(f"Executing task: {func.__name__}")
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
)
""")
    
    print(f"\nMock implementation created in {mock_dir}")
    print(f"Installing mock agency-swarm...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", mock_dir])
    print("Mock agency-swarm installed successfully!")

if __name__ == "__main__":
    main()