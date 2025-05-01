"""
Test Script for Instagram Automation Tool Agents
-----------------------------------------------
This script tests the functionality of each agent and verifies
that they can communicate with each other properly.
"""

import logging
import time
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the Instagram Automation Tool
from instagram_automation_tool import InstagramAutomationTool

def test_account_manager_agent():
    """Test the AccountManagerAgent functionality."""
    logger.info("Testing AccountManagerAgent...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Test account creation
    account = tool.create_account(
        username="test_user",
        password="TestPassword123!",
        email="test@example.com"
    )
    logger.info(f"Account created with ID: {account['id']}")
    assert account['username'] == "test_user", "Account username doesn't match"
    
    # Test profile setup
    profile_result = tool.setup_profile(
        account_id=account["id"],
        bio="Test bio",
        profile_pic="test_pic.jpg",
        external_link="https://example.com"
    )
    logger.info("Profile setup completed")
    assert profile_result['status'] == "success", "Profile setup failed"
    
    # Test account health check
    health_result = tool.agency.get_agent("AccountManagerAgent").check_account_health(
        account_id=account["id"]
    )
    logger.info(f"Account health status: {health_result['health']['status']}")
    assert 'health' in health_result, "Health check failed"
    
    logger.info("AccountManagerAgent tests passed")
    return account

def test_messaging_agent(account_id):
    """Test the MessagingAgent functionality."""
    logger.info("Testing MessagingAgent...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Test campaign creation
    campaign = tool.create_messaging_campaign(
        account_ids=[account_id],
        target_source="follower_list",
        target_details={
            "account_to_scrape": "test_account",
            "name": "Test Campaign"
        },
        message_templates=[
            {
                "id": "template_1",
                "content": "Hi there! This is a test message.",
                "sequence_position": 1
            }
        ],
        use_cupidbot=False
    )
    logger.info(f"Campaign created with ID: {campaign['id']}")
    assert campaign['account_ids'] == [account_id], "Campaign account IDs don't match"
    
    # Test campaign start
    start_result = tool.agency.get_agent("MessagingAgent").start_campaign(
        campaign_id=campaign["id"]
    )
    logger.info(f"Campaign started: {start_result['status']}")
    assert start_result['status'] == "active", "Campaign not active"
    
    # Test message sending
    message_result = tool.agency.get_agent("MessagingAgent").send_message(
        account_id=account_id,
        target_username="test_target",
        message_template={"content": "Hi there! This is a test message."},
        use_cupidbot=False
    )
    logger.info(f"Message sent: {message_result['message_sent']}")
    assert message_result['message_sent'] == True, "Message not sent"
    
    logger.info("MessagingAgent tests passed")
    return campaign

def test_content_poster_agent(account_id):
    """Test the ContentPosterAgent functionality."""
    logger.info("Testing ContentPosterAgent...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Test post creation
    post = tool.create_post(
        account_id=account_id,
        media_paths=["test_image.jpg"],
        caption="Test caption",
        hashtags=["test", "example"],
        scheduled_time=None  # Post immediately
    )
    logger.info(f"Post created with ID: {post['id']}")
    assert post['account_id'] == account_id, "Post account ID doesn't match"
    
    # Test post performance tracking
    performance = tool.agency.get_agent("ContentPosterAgent").track_post_performance(
        post_id=post["id"]
    )
    logger.info(f"Post performance tracked: {performance['post_id']}")
    assert performance['post_id'] == post["id"], "Post ID doesn't match"
    
    # Test batch post creation
    batch_result = tool.agency.get_agent("ContentPosterAgent").create_batch_posts(
        account_id=account_id,
        posts_data=[
            {
                "media_paths": ["test_image1.jpg"],
                "caption": "Test caption 1",
                "hashtags": ["test1"]
            },
            {
                "media_paths": ["test_image2.jpg"],
                "caption": "Test caption 2",
                "hashtags": ["test2"]
            }
        ]
    )
    logger.info(f"Batch posts created: {batch_result['posts_created']}")
    assert batch_result['posts_created'] == 2, "Incorrect number of posts created"
    
    logger.info("ContentPosterAgent tests passed")
    return post

def test_browser_manager_agent():
    """Test the BrowserManagerAgent functionality."""
    logger.info("Testing BrowserManagerAgent...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    browser_manager = tool.agency.get_agent("BrowserManagerAgent")
    
    # Test browser profile creation
    profile = browser_manager.create_browser_profile(
        profile_name="test_profile"
    )
    logger.info(f"Browser profile created: {profile['profile_id']}")
    assert profile['status'] == "created", "Browser profile not created"
    
    # Test browser opening
    browser_session = browser_manager.open_browser(
        profile_id=profile["profile_id"]
    )
    logger.info(f"Browser opened: {browser_session['status']}")
    assert browser_session['status'] == "running", "Browser not running"
    
    # Test navigation
    navigation_result = browser_manager.navigate(
        profile_id=profile["profile_id"],
        url="https://www.instagram.com"
    )
    logger.info(f"Navigation result: {navigation_result['status']}")
    assert navigation_result['status'] == "success", "Navigation failed"
    
    # Test action performance
    action_result = browser_manager.perform_action(
        profile_id=profile["profile_id"],
        action_type="click",
        action_params={"selector": ".login-button"}
    )
    logger.info(f"Action performed: {action_result['status']}")
    assert action_result['status'] == "success", "Action failed"
    
    # Test browser closing
    close_result = browser_manager.close_browser(
        profile_id=profile["profile_id"]
    )
    logger.info(f"Browser closed: {close_result['status']}")
    assert close_result['status'] == "stopped", "Browser not stopped"
    
    logger.info("BrowserManagerAgent tests passed")
    return profile

def test_agent_communication():
    """Test communication between agents."""
    logger.info("Testing agent communication...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Test AccountManagerAgent -> BrowserManagerAgent communication
    logger.info("Testing AccountManagerAgent -> BrowserManagerAgent communication...")
    account = tool.create_account(
        username="comm_test_user",
        password="TestPassword123!",
        email="comm_test@example.com"
    )
    logger.info(f"Account created with ID: {account['id']}")
    
    # Test MessagingAgent -> BrowserManagerAgent communication
    logger.info("Testing MessagingAgent -> BrowserManagerAgent communication...")
    campaign = tool.create_messaging_campaign(
        account_ids=[account['id']],
        target_source="follower_list",
        target_details={
            "account_to_scrape": "comm_test_account",
            "name": "Communication Test Campaign"
        },
        message_templates=[
            {
                "id": "template_1",
                "content": "Hi there! This is a communication test message.",
                "sequence_position": 1
            }
        ],
        use_cupidbot=True
    )
    
    # Test CupidBot activation (MessagingAgent -> BrowserManagerAgent)
    message_result = tool.agency.get_agent("MessagingAgent").send_message(
        account_id=account['id'],
        target_username="comm_test_target",
        message_template={"content": "Hi there! This is a communication test message."},
        use_cupidbot=True
    )
    logger.info(f"Message sent with CupidBot: {message_result['cupidbot_activated']}")
    assert message_result['cupidbot_activated'] == True, "CupidBot not activated"
    
    # Test ContentPosterAgent -> BrowserManagerAgent communication
    logger.info("Testing ContentPosterAgent -> BrowserManagerAgent communication...")
    post = tool.create_post(
        account_id=account['id'],
        media_paths=["comm_test_image.jpg"],
        caption="Communication test caption",
        hashtags=["comm_test"],
        scheduled_time=None  # Post immediately
    )
    logger.info(f"Post created with ID: {post['id']}")
    
    logger.info("Agent communication tests passed")

def main():
    """Run all agent tests."""
    logger.info("Starting agent tests...")
    
    try:
        # Test individual agents
        account = test_account_manager_agent()
        campaign = test_messaging_agent(account['id'])
        post = test_content_poster_agent(account['id'])
        profile = test_browser_manager_agent()
        
        # Test agent communication
        test_agent_communication()
        
        logger.info("All agent tests passed!")
        
    except AssertionError as e:
        logger.error(f"Test failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()