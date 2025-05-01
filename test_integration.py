#!/usr/bin/env python3
"""
Integration Test Script for Instagram Automation Tool
----------------------------------------------------
This script tests the integration of all components of the Instagram Automation Tool.
"""

import os
import sys
import logging
import json
import time
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('integration_test.log')
    ]
)
logger = logging.getLogger(__name__)

# Import the Instagram Automation Tool
from instagram_automation_tool import InstagramAutomationTool

def test_run_command():
    """Test the 'run' command."""
    logger.info("=== Testing 'run' command ===")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Run the tool (just initialize it, don't actually run the main loop)
    logger.info("Starting Instagram Automation Tool")
    
    # Check if the agency is properly set up
    if tool.agency:
        logger.info("Agency initialized successfully")
        
        # Check if all agents are available
        agents = [
            "AccountManagerAgent",
            "MessagingAgent",
            "ContentPosterAgent",
            "BrowserManagerAgent"
        ]
        
        all_agents_available = True
        for agent_name in agents:
            agent = tool.agency.get_agent(agent_name)
            if agent:
                logger.info(f"Agent '{agent_name}' is available")
            else:
                logger.error(f"Agent '{agent_name}' is not available")
                all_agents_available = False
        
        if all_agents_available:
            logger.info("All agents are available")
            return True
        else:
            logger.error("Some agents are not available")
            return False
    else:
        logger.error("Agency initialization failed")
        return False

def test_account_command():
    """Test the 'account' commands."""
    logger.info("=== Testing 'account' commands ===")
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Test account creation
    logger.info("Testing account creation")
    account = tool.create_account(
        username="test_user_" + str(int(time.time())),
        password="TestPassword123!",
        email="test_" + str(int(time.time())) + "@example.com",
        phone=None
    )
    
    if account and "id" in account:
        logger.info(f"Account created successfully: {account['id']}")
        
        # Test profile setup
        logger.info("Testing profile setup")
        profile_result = tool.setup_profile(
            account_id=account["id"],
            bio="This is a test profile",
            profile_pic="",
            external_link="https://example.com"
        )
        
        if profile_result and profile_result.get("status") == "success":
            logger.info("Profile setup successful")
            
            # Test account health check
            logger.info("Testing account health check")
            health_result = tool.agency.get_agent("AccountManagerAgent").check_account_health(
                account_id=account["id"]
            )
            
            if health_result and "health" in health_result:
                logger.info(f"Account health status: {health_result['health']['status']}")
                return True, account["id"]
            else:
                logger.error("Account health check failed")
                return False, account["id"]
        else:
            logger.error("Profile setup failed")
            return False, account["id"]
    else:
        logger.error("Account creation failed")
        return False, None

def test_message_command(account_id):
    """Test the 'message' commands."""
    logger.info("=== Testing 'message' commands ===")
    
    if not account_id:
        logger.error("No account ID provided for message test")
        return False
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Test campaign creation
    logger.info("Testing messaging campaign creation")
    
    # Create target details
    target_details = {
        "name": "Test Campaign",
        "account_to_scrape": "instagram"
    }
    
    # Create message templates
    message_templates = [
        {
            "name": "Initial Message",
            "content": "Hi there! I saw your profile and thought it was interesting.",
            "delay": {"min": 1, "max": 3}
        },
        {
            "name": "Follow-up",
            "content": "Would you be interested in connecting?",
            "delay": {"min": 5, "max": 10}
        }
    ]
    
    # Create campaign
    campaign = tool.create_messaging_campaign(
        account_ids=[account_id],
        target_source="follower_list",
        target_details=target_details,
        message_templates=message_templates,
        use_cupidbot=True
    )
    
    if campaign and "id" in campaign:
        logger.info(f"Campaign created successfully: {campaign['id']}")
        
        # Test campaign start
        logger.info("Testing campaign start")
        start_result = tool.agency.get_agent("MessagingAgent").start_campaign(
            campaign_id=campaign["id"]
        )
        
        if start_result and start_result.get("status") == "active":
            logger.info(f"Campaign started successfully: {campaign['id']}")
            return True, campaign["id"]
        else:
            logger.error("Campaign start failed")
            return False, campaign["id"]
    else:
        logger.error("Campaign creation failed")
        return False, None

def test_post_command(account_id):
    """Test the 'post' commands."""
    logger.info("=== Testing 'post' commands ===")
    
    if not account_id:
        logger.error("No account ID provided for post test")
        return False
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Test post creation
    logger.info("Testing post creation")
    
    # Create a dummy media file for testing
    media_path = "test_media.jpg"
    with open(media_path, "w") as f:
        f.write("This is a dummy image file for testing")
    
    # Create post
    post = tool.create_post(
        account_id=account_id,
        media_paths=[media_path],
        caption="This is a test post",
        hashtags=["test", "instagram", "automation"],
        tagged_users=[],
        location="Test Location",
        scheduled_time=None  # Post immediately
    )
    
    # Clean up the dummy media file
    try:
        os.remove(media_path)
    except:
        pass
    
    if post and "id" in post:
        logger.info(f"Post created successfully: {post['id']}")
        
        # Test post performance tracking
        logger.info("Testing post performance tracking")
        performance_result = tool.agency.get_agent("ContentPosterAgent").track_post_performance(
            post_id=post["id"]
        )
        
        if performance_result and "performance" in performance_result:
            logger.info(f"Post performance tracked successfully: {post['id']}")
            return True, post["id"]
        else:
            logger.error("Post performance tracking failed")
            return False, post["id"]
    else:
        logger.error("Post creation failed")
        return False, None

def run_integration_test():
    """Run the full integration test."""
    logger.info("Starting Instagram Automation Tool Integration Test")
    
    # Test results
    results = {
        "run_command": False,
        "account_command": False,
        "message_command": False,
        "post_command": False
    }
    
    # Test the 'run' command
    results["run_command"] = test_run_command()
    
    # Test the 'account' commands
    account_result, account_id = test_account_command()
    results["account_command"] = account_result
    
    # Test the 'message' commands
    if account_id:
        message_result, campaign_id = test_message_command(account_id)
        results["message_command"] = message_result
    
    # Test the 'post' commands
    if account_id:
        post_result, post_id = test_post_command(account_id)
        results["post_command"] = post_result
    
    # Print summary
    logger.info("=== Integration Test Summary ===")
    logger.info(f"Run Command Test: {'PASSED' if results['run_command'] else 'FAILED'}")
    logger.info(f"Account Command Test: {'PASSED' if results['account_command'] else 'FAILED'}")
    logger.info(f"Message Command Test: {'PASSED' if results['message_command'] else 'FAILED'}")
    logger.info(f"Post Command Test: {'PASSED' if results['post_command'] else 'FAILED'}")
    
    all_passed = all(results.values())
    logger.info(f"Overall Integration Test: {'PASSED' if all_passed else 'FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    run_integration_test()