"""
Example Script for Instagram Automation Tool
-------------------------------------------
This script demonstrates how to use the Instagram Automation Tool
with a complete workflow example.
"""

import time
import logging
from datetime import datetime, timedelta
from instagram_automation_tool import InstagramAutomationTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run a complete example workflow."""
    logger.info("Starting Instagram Automation Tool example")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Step 1: Create a new Instagram account
    logger.info("Step 1: Creating a new Instagram account")
    account = tool.create_account(
        username="example_user_2025",
        password="SecurePassword123!",
        email="example2025@tempmail.com"
    )
    logger.info(f"Account created with ID: {account['id']}")
    
    # Step 2: Set up the profile
    logger.info("Step 2: Setting up the profile")
    profile_result = tool.setup_profile(
        account_id=account["id"],
        bio="Digital creator | Photography enthusiast | Nature lover",
        profile_pic="profile_pic.jpg",  # Assumes a file in the current directory
        external_link="https://example.com/photography"
    )
    logger.info("Profile setup completed")
    
    # Step 3: Create and schedule a post
    logger.info("Step 3: Creating and scheduling a post")
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_noon = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    
    post = tool.create_post(
        account_id=account["id"],
        media_paths=["sunset.jpg", "beach.jpg"],  # Assumes files in the current directory
        caption="Enjoying the beautiful sunset at the beach. What's your favorite time of day?",
        hashtags=["sunset", "beachlife", "naturephotography", "views"],
        tagged_users=[],
        location="Malibu Beach",
        scheduled_time=tomorrow_noon
    )
    logger.info(f"Post scheduled with ID: {post['id']} for {tomorrow_noon}")
    
    # Step 4: Create a messaging campaign
    logger.info("Step 4: Creating a messaging campaign")
    campaign = tool.create_messaging_campaign(
        account_ids=[account["id"]],
        target_source="follower_list",
        target_details={
            "account_to_scrape": "photography_community",
            "name": "Photography Enthusiasts Campaign"
        },
        message_templates=[
            {
                "id": "template_1",
                "content": "Hi there! I love your photography style. Just wanted to connect with fellow photographers. What camera do you use?",
                "sequence_position": 1
            },
            {
                "id": "template_2",
                "content": "Thanks for the response! I'm currently using a Sony Alpha. Have you checked out my latest sunset collection?",
                "sequence_position": 2
            }
        ],
        use_cupidbot=True
    )
    logger.info(f"Campaign created with ID: {campaign['id']}")
    
    # Step 5: Start the campaign
    logger.info("Step 5: Starting the messaging campaign")
    start_result = tool.agency.get_agent("MessagingAgent").start_campaign(
        campaign_id=campaign["id"],
        start_time=datetime.now() + timedelta(hours=1)
    )
    logger.info(f"Campaign scheduled to start at {start_result.get('scheduled_start')}")
    
    # Step 6: Monitor account health
    logger.info("Step 6: Monitoring account health")
    health_result = tool.agency.get_agent("AccountManagerAgent").check_account_health(
        account_id=account["id"]
    )
    logger.info(f"Account health status: {health_result['health']['status']}")
    
    logger.info("Example workflow completed successfully")
    logger.info("In a real scenario, the tool would continue running to:")
    logger.info("- Execute the scheduled post at the specified time")
    logger.info("- Run the messaging campaign when scheduled")
    logger.info("- Monitor responses and engage with CupidBot")
    logger.info("- Track performance metrics")

if __name__ == "__main__":
    main()