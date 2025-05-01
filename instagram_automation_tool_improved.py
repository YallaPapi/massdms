"""
Instagram Automation Tool (Improved)
----------------------------------
A comprehensive solution for automating Instagram account management, messaging, and content posting.
Built using agency-swarm framework for multi-agent collaboration.

This improved version includes wrapper methods for all agent operations to provide a more
consistent API and better error handling.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('instagram_automation.log')
    ]
)
logger = logging.getLogger(__name__)

# Try to import agency-swarm
try:
    from agency_swarm import Agency, Agent
except ImportError:
    logger.error("agency-swarm package not found. Please install it using: pip install agency-swarm")
    sys.exit(1)

# Import our custom agents
from agents.account_manager import AccountManagerAgent
from agents.messaging_agent import MessagingAgent
from agents.content_poster import ContentPosterAgent
from agents.browser_manager import BrowserManagerAgent

# Import utilities
from utils.config_loader import load_config
from utils.database import Database

class InstagramAutomationTool:
    """Main class for the Instagram Automation Tool."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the Instagram Automation Tool.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config = load_config(config_path)
        self.db = Database(self.config.get("database", {}))
        self.agency = self._setup_agency()
        logger.info("Instagram Automation Tool initialized")
    
    def _setup_agency(self) -> Agency:
        """Set up the agency with all required agents.
        
        Returns:
            Agency: Configured agency with all agents
        """
        # Create agents
        account_manager = AccountManagerAgent()
        messaging_agent = MessagingAgent()
        content_poster = ContentPosterAgent()
        browser_manager = BrowserManagerAgent()
        
        # Create agency
        agency = Agency(
            name="Instagram Automation Agency",
            description="An agency for automating Instagram operations",
            agents=[
                account_manager,
                messaging_agent,
                content_poster,
                browser_manager
            ]
        )
        
        # Define agent relationships
        agency.add_communication(account_manager, messaging_agent)
        agency.add_communication(account_manager, content_poster)
        agency.add_communication(account_manager, browser_manager)
        agency.add_communication(messaging_agent, browser_manager)
        agency.add_communication(content_poster, browser_manager)
        
        return agency
    
    # Account Management Methods
    
    def create_account(self, username: str, password: str, email: str, phone: Optional[str] = None) -> Dict[str, Any]:
        """Create a new Instagram account.
        
        Args:
            username: Desired username for the account
            password: Password for the account
            email: Email for verification
            phone: Optional phone number for verification
            
        Returns:
            Dict containing account information
        """
        logger.info(f"Creating new account with username: {username}")
        try:
            result = self.agency.get_agent("AccountManagerAgent").create_account(
                username=username,
                password=password,
                email=email,
                phone=phone
            )
            return result
        except Exception as e:
            logger.error(f"Error creating account: {str(e)}")
            return {"status": "error", "message": f"Failed to create account: {str(e)}"}
    
    def setup_profile(self, account_id: str, bio: str = "", profile_pic: str = "", 
                     external_link: str = "") -> Dict[str, Any]:
        """Set up an Instagram profile.
        
        Args:
            account_id: ID of the account to set up
            bio: Biography text
            profile_pic: Path to profile picture
            external_link: External link for bio
            
        Returns:
            Dict containing profile setup result
        """
        logger.info(f"Setting up profile for account: {account_id}")
        try:
            result = self.agency.get_agent("AccountManagerAgent").setup_profile(
                account_id=account_id,
                bio=bio,
                profile_pic=profile_pic,
                external_link=external_link
            )
            return result
        except Exception as e:
            logger.error(f"Error setting up profile: {str(e)}")
            return {"status": "error", "message": f"Failed to set up profile: {str(e)}"}
    
    def check_account_health(self, account_id: str) -> Dict[str, Any]:
        """Check the health status of an account.
        
        Args:
            account_id: ID of the account to check
            
        Returns:
            Dict containing account health information
        """
        logger.info(f"Checking health for account: {account_id}")
        try:
            result = self.agency.get_agent("AccountManagerAgent").check_account_health(
                account_id=account_id
            )
            return result
        except Exception as e:
            logger.error(f"Error checking account health: {str(e)}")
            return {"status": "error", "message": f"Failed to check account health: {str(e)}"}
    
    # Messaging Methods
    
    def create_messaging_campaign(self, account_ids: List[str], target_source: str, 
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
        try:
            result = self.agency.get_agent("MessagingAgent").create_campaign(
                account_ids=account_ids,
                target_source=target_source,
                target_details=target_details,
                message_templates=message_templates,
                use_cupidbot=use_cupidbot
            )
            return result
        except Exception as e:
            logger.error(f"Error creating messaging campaign: {str(e)}")
            return {"status": "error", "message": f"Failed to create messaging campaign: {str(e)}"}
    
    def start_campaign(self, campaign_id: str, start_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Start a messaging campaign.
        
        Args:
            campaign_id: ID of the campaign to start
            start_time: Optional time to start the campaign (None for immediate start)
            
        Returns:
            Dict containing campaign start result
        """
        logger.info(f"Starting campaign: {campaign_id}")
        try:
            result = self.agency.get_agent("MessagingAgent").start_campaign(
                campaign_id=campaign_id,
                start_time=start_time
            )
            return result
        except Exception as e:
            logger.error(f"Error starting campaign: {str(e)}")
            return {"status": "error", "message": f"Failed to start campaign: {str(e)}"}
    
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
        try:
            result = self.agency.get_agent("MessagingAgent").send_message(
                account_id=account_id,
                target_username=target_username,
                message_template=message_template,
                use_cupidbot=use_cupidbot
            )
            return result
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return {"status": "error", "message": f"Failed to send message: {str(e)}"}
    
    # Content Posting Methods
    
    def create_post(self, account_id: str, media_paths: List[str], caption: str,
                   hashtags: List[str] = [], tagged_users: List[str] = [],
                   location: str = "", scheduled_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Create and schedule a post.
        
        Args:
            account_id: ID of the account to post from
            media_paths: Paths to media files (images/videos)
            caption: Post caption
            hashtags: List of hashtags
            tagged_users: List of users to tag
            location: Location tag
            scheduled_time: When to publish the post
            
        Returns:
            Dict containing post information
        """
        logger.info(f"Creating post for account: {account_id}")
        try:
            result = self.agency.get_agent("ContentPosterAgent").create_post(
                account_id=account_id,
                media_paths=media_paths,
                caption=caption,
                hashtags=hashtags,
                tagged_users=tagged_users,
                location=location,
                scheduled_time=scheduled_time
            )
            return result
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}")
            return {"status": "error", "message": f"Failed to create post: {str(e)}"}
    
    def publish_post(self, post_id: str) -> Dict[str, Any]:
        """Publish a post to Instagram.
        
        Args:
            post_id: ID of the post to publish
            
        Returns:
            Dict containing publish result
        """
        logger.info(f"Publishing post: {post_id}")
        try:
            result = self.agency.get_agent("ContentPosterAgent").publish_post(
                post_id=post_id
            )
            return result
        except Exception as e:
            logger.error(f"Error publishing post: {str(e)}")
            return {"status": "error", "message": f"Failed to publish post: {str(e)}"}
    
    def track_post_performance(self, post_id: str) -> Dict[str, Any]:
        """Track the performance of a published post.
        
        Args:
            post_id: ID of the post to track
            
        Returns:
            Dict containing performance metrics
        """
        logger.info(f"Tracking performance for post: {post_id}")
        try:
            result = self.agency.get_agent("ContentPosterAgent").track_post_performance(
                post_id=post_id
            )
            return result
        except Exception as e:
            logger.error(f"Error tracking post performance: {str(e)}")
            return {"status": "error", "message": f"Failed to track post performance: {str(e)}"}
    
    def create_batch_posts(self, account_id: str, posts_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple posts in a batch.
        
        Args:
            account_id: ID of the account to post from
            posts_data: List of post data dictionaries
            
        Returns:
            Dict containing batch creation result
        """
        logger.info(f"Creating batch of {len(posts_data)} posts for account: {account_id}")
        try:
            result = self.agency.get_agent("ContentPosterAgent").create_batch_posts(
                account_id=account_id,
                posts_data=posts_data
            )
            return result
        except Exception as e:
            logger.error(f"Error creating batch posts: {str(e)}")
            return {"status": "error", "message": f"Failed to create batch posts: {str(e)}"}
    
    # Main Application Methods
    
    def run(self):
        """Run the Instagram Automation Tool."""
        logger.info("Starting Instagram Automation Tool")
        try:
            # Main application logic here
            
            # Example: Print status
            print("Instagram Automation Tool is running")
            print(f"Configured with {len(self.config.get('accounts', []))} accounts")
            
            # Here you would implement the main loop or server
            # that handles user commands, scheduled tasks, etc.
        except Exception as e:
            logger.error(f"Error running Instagram Automation Tool: {str(e)}")
            return {"status": "error", "message": f"Failed to run Instagram Automation Tool: {str(e)}"}

if __name__ == "__main__":
    # Create and run the tool
    tool = InstagramAutomationTool()
    tool.run()