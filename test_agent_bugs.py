"""
Test Script for Instagram Automation Tool Agent Bugs
---------------------------------------------------
This script tests for potential bugs in the agent implementations.
"""

import logging
import time
import random
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the Instagram Automation Tool
from instagram_automation_tool import InstagramAutomationTool

def test_account_manager_edge_cases():
    """Test edge cases for the AccountManagerAgent."""
    logger.info("Testing AccountManagerAgent edge cases...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    account_manager = tool.agency.get_agent("AccountManagerAgent")
    
    # Test case 1: Create account with empty username
    try:
        account = account_manager.create_account(
            username="",
            password="TestPassword123!",
            email="empty_username@example.com"
        )
        logger.warning("Empty username was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Empty username correctly rejected: {e}")
    
    # Test case 2: Create account with very long username
    long_username = "a" * 100  # Instagram has a username length limit
    try:
        account = account_manager.create_account(
            username=long_username,
            password="TestPassword123!",
            email="long_username@example.com"
        )
        logger.warning("Very long username was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Long username correctly rejected: {e}")
    
    # Test case 3: Setup profile for non-existent account
    try:
        profile_result = account_manager.setup_profile(
            account_id="non_existent_account_id",
            bio="Test bio",
            profile_pic="test_pic.jpg",
            external_link="https://example.com"
        )
        logger.warning("Setup profile for non-existent account was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Setup profile for non-existent account correctly rejected: {e}")
    
    logger.info("AccountManagerAgent edge case tests completed")

def test_messaging_agent_edge_cases():
    """Test edge cases for the MessagingAgent."""
    logger.info("Testing MessagingAgent edge cases...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    messaging_agent = tool.agency.get_agent("MessagingAgent")
    
    # Create a test account for messaging tests
    account = tool.create_account(
        username="messaging_test_user",
        password="TestPassword123!",
        email="messaging_test@example.com"
    )
    
    # Test case 1: Create campaign with empty account IDs
    try:
        campaign = messaging_agent.create_campaign(
            account_ids=[],
            target_source="follower_list",
            target_details={
                "account_to_scrape": "test_account",
                "name": "Empty Accounts Campaign"
            },
            message_templates=[
                {
                    "id": "template_1",
                    "content": "Test message",
                    "sequence_position": 1
                }
            ]
        )
        logger.warning("Campaign with empty account IDs was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Campaign with empty account IDs correctly rejected: {e}")
    
    # Test case 2: Create campaign with invalid target source
    try:
        campaign = messaging_agent.create_campaign(
            account_ids=[account['id']],
            target_source="invalid_source",
            target_details={
                "name": "Invalid Source Campaign"
            },
            message_templates=[
                {
                    "id": "template_1",
                    "content": "Test message",
                    "sequence_position": 1
                }
            ]
        )
        logger.warning("Campaign with invalid target source was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Campaign with invalid target source correctly rejected: {e}")
    
    # Test case 3: Start non-existent campaign
    try:
        start_result = messaging_agent.start_campaign(
            campaign_id="non_existent_campaign_id"
        )
        logger.warning("Starting non-existent campaign was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Starting non-existent campaign correctly rejected: {e}")
    
    logger.info("MessagingAgent edge case tests completed")

def test_content_poster_edge_cases():
    """Test edge cases for the ContentPosterAgent."""
    logger.info("Testing ContentPosterAgent edge cases...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    content_poster = tool.agency.get_agent("ContentPosterAgent")
    
    # Create a test account for content tests
    account = tool.create_account(
        username="content_test_user",
        password="TestPassword123!",
        email="content_test@example.com"
    )
    
    # Test case 1: Create post with empty media paths
    try:
        post = content_poster.create_post(
            account_id=account['id'],
            media_paths=[],
            caption="Test caption"
        )
        logger.warning("Post with empty media paths was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Post with empty media paths correctly rejected: {e}")
    
    # Test case 2: Create post with invalid media paths
    try:
        post = content_poster.create_post(
            account_id=account['id'],
            media_paths=["non_existent_image.jpg"],
            caption="Test caption"
        )
        logger.warning("Post with invalid media paths was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Post with invalid media paths correctly rejected: {e}")
    
    # Test case 3: Track performance of non-existent post
    try:
        performance = content_poster.track_post_performance(
            post_id="non_existent_post_id"
        )
        logger.warning("Tracking non-existent post was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Tracking non-existent post correctly rejected: {e}")
    
    logger.info("ContentPosterAgent edge case tests completed")

def test_browser_manager_edge_cases():
    """Test edge cases for the BrowserManagerAgent."""
    logger.info("Testing BrowserManagerAgent edge cases...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    browser_manager = tool.agency.get_agent("BrowserManagerAgent")
    
    # Test case 1: Open browser with non-existent profile
    try:
        browser_session = browser_manager.open_browser(
            profile_id="non_existent_profile_id"
        )
        logger.warning("Opening browser with non-existent profile was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Opening browser with non-existent profile correctly rejected: {e}")
    
    # Test case 2: Navigate with non-existent profile
    try:
        navigation_result = browser_manager.navigate(
            profile_id="non_existent_profile_id",
            url="https://www.instagram.com"
        )
        logger.warning("Navigating with non-existent profile was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Navigating with non-existent profile correctly rejected: {e}")
    
    # Test case 3: Close non-existent browser
    try:
        close_result = browser_manager.close_browser(
            profile_id="non_existent_profile_id"
        )
        logger.warning("Closing non-existent browser was accepted, which might be a bug")
    except Exception as e:
        logger.info(f"Closing non-existent browser correctly rejected: {e}")
    
    logger.info("BrowserManagerAgent edge case tests completed")

def test_concurrent_operations():
    """Test concurrent operations to check for race conditions."""
    logger.info("Testing concurrent operations...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Create a test account
    account = tool.create_account(
        username="concurrent_test_user",
        password="TestPassword123!",
        email="concurrent_test@example.com"
    )
    
    # Simulate concurrent operations on the same account
    # In a real test, this would use threading or multiprocessing
    
    # Operation 1: Set up profile
    profile_result = tool.setup_profile(
        account_id=account["id"],
        bio="Concurrent test bio",
        profile_pic="concurrent_test_pic.jpg",
        external_link="https://example.com/concurrent"
    )
    
    # Operation 2: Create a post
    post = tool.create_post(
        account_id=account["id"],
        media_paths=["concurrent_test_image.jpg"],
        caption="Concurrent test caption",
        hashtags=["concurrent", "test"]
    )
    
    # Operation 3: Check account health
    health_result = tool.agency.get_agent("AccountManagerAgent").check_account_health(
        account_id=account["id"]
    )
    
    logger.info("Concurrent operations test completed")

def test_error_handling():
    """Test error handling in the agents."""
    logger.info("Testing error handling...")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Test case 1: Handle network errors in BrowserManagerAgent
    browser_manager = tool.agency.get_agent("BrowserManagerAgent")
    
    # Temporarily change the API URL to simulate a network error
    original_url = browser_manager.adspower_api_url
    browser_manager.adspower_api_url = "http://invalid-url:12345"
    
    try:
        profile = browser_manager.create_browser_profile(
            profile_name="error_test_profile"
        )
        logger.warning("Network error was not handled properly")
    except Exception as e:
        logger.info(f"Network error correctly handled: {e}")
    finally:
        # Restore the original URL
        browser_manager.adspower_api_url = original_url
    
    # Test case 2: Handle invalid parameters
    try:
        account = tool.create_account(
            username=None,  # Invalid parameter
            password="TestPassword123!",
            email="error_test@example.com"
        )
        logger.warning("Invalid parameter was not handled properly")
    except Exception as e:
        logger.info(f"Invalid parameter correctly handled: {e}")
    
    logger.info("Error handling tests completed")

def main():
    """Run all agent bug tests."""
    logger.info("Starting agent bug tests...")
    
    try:
        # Test edge cases for each agent
        test_account_manager_edge_cases()
        test_messaging_agent_edge_cases()
        test_content_poster_edge_cases()
        test_browser_manager_edge_cases()
        
        # Test concurrent operations
        test_concurrent_operations()
        
        # Test error handling
        test_error_handling()
        
        logger.info("All agent bug tests completed!")
        
    except Exception as e:
        logger.error(f"Unexpected error in tests: {e}")

if __name__ == "__main__":
    main()