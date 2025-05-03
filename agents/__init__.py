"""
Instagram Automation Tool - Agents Package
-----------------------------------------
This package contains the agents used by the Instagram Automation Tool.
"""

# Import the Agent and Task base classes
from utils.agent_base import Agent, Task

# Import agent implementations
from agents.account_manager import AccountManagerAgent
from agents.messaging_agent import MessagingAgent
from agents.content_poster import ContentPosterAgent
from agents.browser_manager import BrowserManagerAgent

__all__ = [
    'Agent',
    'Task',
    'AccountManagerAgent',
    'MessagingAgent',
    'ContentPosterAgent',
    'BrowserManagerAgent'
]