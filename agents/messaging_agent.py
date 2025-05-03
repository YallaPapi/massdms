"""
Messaging Agent
--------------
Responsible for managing Instagram direct messaging campaigns, including:
- Target audience selection
- Message template management
- Campaign execution
- CupidBot integration for AI conversations
"""

import logging
import time
import random
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import from utils instead to avoid circular imports
from utils.agent_base import Agent, Task

logger = logging.getLogger(__name__)

class MessagingAgent(Agent):
    """Agent responsible for Instagram direct messaging campaigns."""
    
    def __init__(self):
        """Initialize the Messaging Agent."""
        super().__init__(
            name="MessagingAgent",
            description="Manages Instagram direct messaging campaigns",
            instructions="""
            You are responsible for managing Instagram direct messaging campaigns.
            Your tasks include:
            1. Selecting target audiences from follower lists or imported files
            2. Creating and managing message templates
            3. Executing messaging campaigns
            4. Integrating with CupidBot for AI-powered conversations
            
            Always ensure messages appear authentic and personalized to avoid detection.
            Implement proper delays between messages to mimic human behavior.
            """
        )
    
    @Task
    def create_campaign(self, account_ids: List[str], target_source: str, 
                       target_details: Dict[str, Any], message_templates: List[Dict[str, Any]],
                       use_cupidbot: bool = False) -> Dict[str, Any]:
        """Create a new messaging campaign.
        
        Args:
            account_ids: List of account IDs to use for messaging
            target_source: Source of target users ('follower_list' or 'text_file')
            target_details: Details about the target source
            message_templates: List of message templates
            use_cupidbot: Whether to use CupidBot for AI conversations
            
        Returns:
            Dict containing campaign information
        """
        logger.info(f"Creating messaging campaign for {len(account_ids)} accounts")
        
        # Generate campaign ID
        campaign_id = f"campaign_{int(time.time())}"
        
        # Process target audience
        target_users = self._get_target_users(target_source, target_details)
        
        # Create campaign record
        campaign = {
            "id": campaign_id,
            "name": target_details.get("name", f"Campaign {campaign_id}"),
            "account_ids": account_ids,
            "target_source": target_source,
            "target_source_details": target_details,
            "target_users": target_users[:10],  # Store first 10 for preview
            "target_user_count": len(target_users),
            "message_templates": message_templates,
            "use_cupidbot": use_cupidbot,
            "cupidbot_settings": {
                "personality": "friendly",
                "response_style": "casual"
            } if use_cupidbot else None,
            "status": "draft",
            "stats": {
                "messages_sent": 0,
                "responses_received": 0,
                "conversion_rate": 0
            },
            "created_at": time.time(),
            "scheduled_start": None,
            "last_run": None
        }
        
        logger.info(f"Campaign created: {campaign_id} with {len(target_users)} target users")
        return campaign
    
    def _get_target_users(self, target_source: str, target_details: Dict[str, Any]) -> List[str]:
        """Get target users based on the specified source.
        
        Args:
            target_source: Source of target users ('follower_list' or 'text_file')
            target_details: Details about the target source
            
        Returns:
            List of target usernames
        """
        if target_source == "follower_list":
            # Get followers from specified account
            account_to_scrape = target_details.get("account_to_scrape")
            logger.info(f"Scraping followers from account: {account_to_scrape}")
            
            # In a real implementation, this would:
            # 1. Use browser manager to log into an account
            # 2. Navigate to the target account's follower list
            # 3. Scrape followers with proper pagination
            
            # Simulate follower scraping
            time.sleep(random.uniform(2.0, 5.0))  # Simulate scraping time
            
            # Generate dummy follower list for demonstration
            follower_count = random.randint(50, 200)
            followers = [f"user_{i}" for i in range(1, follower_count + 1)]
            
            return followers
            
        elif target_source == "text_file":
            # Import users from text file
            file_path = target_details.get("file_path")
            logger.info(f"Importing users from file: {file_path}")
            
            # In a real implementation, this would read from the actual file
            # For demonstration, we'll simulate file reading
            
            # Simulate file reading
            time.sleep(random.uniform(0.5, 1.5))  # Simulate file reading time
            
            # Generate dummy user list for demonstration
            user_count = random.randint(50, 200)
            users = [f"imported_user_{i}" for i in range(1, user_count + 1)]
            
            return users
        
        else:
            logger.error(f"Unknown target source: {target_source}")
            return []
    
    @Task
    def start_campaign(self, campaign_id: str, start_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Start a messaging campaign.
        
        Args:
            campaign_id: ID of the campaign to start
            start_time: Optional time to start the campaign (None for immediate start)
            
        Returns:
            Dict containing campaign start result
        """
        logger.info(f"Starting campaign: {campaign_id}")
        
        # In a real implementation, this would:
        # 1. Retrieve campaign details from database
        # 2. Schedule campaign if start_time is provided
        # 3. Otherwise, begin execution immediately
        
        # Simulate campaign start
        if start_time:
            logger.info(f"Scheduling campaign {campaign_id} to start at {start_time}")
            # In a real implementation, this would add the campaign to a scheduler
            return {
                "campaign_id": campaign_id,
                "status": "scheduled",
                "scheduled_start": start_time.timestamp()
            }
        else:
            logger.info(f"Starting campaign {campaign_id} immediately")
            # Simulate immediate start
            return {
                "campaign_id": campaign_id,
                "status": "active",
                "started_at": time.time()
            }
    
    @Task
    def send_message(self, account_id: str, target_username: str, 
                    message_template: Dict[str, Any], use_cupidbot: bool = False) -> Dict[str, Any]:
        """Send a direct message to a target user.
        
        Args:
            account_id: ID of the account to send from
            target_username: Username of the target user
            message_template: Template for the message
            use_cupidbot: Whether to use CupidBot for AI conversation
            
        Returns:
            Dict containing message send result
        """
        logger.info(f"Sending message from {account_id} to {target_username}")
        
        # In a real implementation, this would:
        # 1. Retrieve account details from database
        # 2. Use browser manager to log into the account
        # 3. Navigate to the target user's profile
        # 4. Open DM interface
        # 5. Send the message
        # 6. Activate CupidBot if enabled
        
        # Simulate message sending
        time.sleep(random.uniform(1.0, 3.0))  # Simulate human timing
        
        message_result = {
            "account_id": account_id,
            "target_username": target_username,
            "message_sent": True,
            "sent_at": time.time(),
            "message_id": f"msg_{int(time.time())}_{random.randint(1000, 9999)}",
            "cupidbot_activated": use_cupidbot
        }
        
        if use_cupidbot:
            # Activate CupidBot for this conversation
            self._activate_cupidbot(account_id, target_username)
        
        logger.info(f"Message sent to {target_username}")
        return message_result
    
    def _activate_cupidbot(self, account_id: str, target_username: str) -> None:
        """Activate CupidBot for a conversation.
        
        Args:
            account_id: ID of the account
            target_username: Username of the target user
        """
        logger.info(f"Activating CupidBot for conversation between {account_id} and {target_username}")
        
        # In a real implementation, this would:
        # 1. Use browser manager to access the AdsPower browser
        # 2. Activate the CupidBot plugin
        # 3. Configure CupidBot for this specific conversation
        
        # Simulate CupidBot activation
        time.sleep(random.uniform(0.5, 1.5))  # Simulate activation time
        
        logger.info(f"CupidBot activated for conversation with {target_username}")