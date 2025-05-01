#!/usr/bin/env python3
"""
Comprehensive Test Script for Instagram Automation Tool CLI
---------------------------------------------------------
This script tests the command-line interface of the Instagram Automation Tool
by mocking the InstagramAutomationTool class and its methods.
"""

import sys
import argparse
import logging
from unittest.mock import MagicMock, patch
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestCLI:
    """Test class for the Instagram Automation Tool CLI."""
    
    def __init__(self):
        """Initialize the test class."""
        self.mock_tool = MagicMock()
        self.setup_mock_methods()
    
    def setup_mock_methods(self):
        """Set up mock methods for the InstagramAutomationTool class."""
        # Account methods
        self.mock_tool.create_account.return_value = {"id": "acc_123", "status": "success"}
        self.mock_tool.setup_profile.return_value = {"account_id": "acc_123", "status": "success"}
        
        # Mock agency and agents
        mock_account_manager = MagicMock()
        mock_account_manager.check_account_health.return_value = {
            "account_id": "acc_123", 
            "health": {"status": "healthy"}
        }
        
        mock_messaging_agent = MagicMock()
        mock_messaging_agent.start_campaign.return_value = {
            "campaign_id": "camp_123", 
            "status": "active"
        }
        
        self.mock_tool.agency = MagicMock()
        self.mock_tool.agency.get_agent.side_effect = lambda agent_name: {
            "AccountManagerAgent": mock_account_manager,
            "MessagingAgent": mock_messaging_agent
        }.get(agent_name, MagicMock())
        
        # Message methods
        self.mock_tool.create_messaging_campaign.return_value = {"id": "camp_123", "status": "draft"}
        
        # Post methods
        self.mock_tool.create_post.return_value = {"id": "post_123", "status": "published"}
        
        # Run method
        self.mock_tool.run.return_value = None
    
    def test_account_create(self):
        """Test the account create command."""
        args = ["account", "create", "--username", "test_user", "--password", "test_pass", "--email", "test@example.com"]
        self.run_test(args)
        
        # Verify the method was called with correct arguments
        self.mock_tool.create_account.assert_called_once_with(
            username="test_user", 
            password="test_pass", 
            email="test@example.com", 
            phone=None
        )
        logger.info("✅ account create command test passed")
    
    def test_account_setup_profile(self):
        """Test the account setup-profile command."""
        args = ["account", "setup-profile", "--account-id", "acc_123", "--bio", "Test bio", "--profile-pic", "pic.jpg"]
        self.run_test(args)
        
        # Verify the method was called with correct arguments
        self.mock_tool.setup_profile.assert_called_once_with(
            account_id="acc_123", 
            bio="Test bio", 
            profile_pic="pic.jpg", 
            external_link=""
        )
        logger.info("✅ account setup-profile command test passed")
    
    def test_account_health(self):
        """Test the account health command."""
        args = ["account", "health", "--account-id", "acc_123"]
        self.run_test(args)
        
        # Verify the method was called with correct arguments
        self.mock_tool.agency.get_agent.assert_called_with("AccountManagerAgent")
        self.mock_tool.agency.get_agent("AccountManagerAgent").check_account_health.assert_called_once_with(
            account_id="acc_123"
        )
        logger.info("✅ account health command test passed")
    
    def test_message_create_campaign(self):
        """Test the message create-campaign command."""
        args = [
            "message", "create-campaign", 
            "--account-ids", "acc_123,acc_456", 
            "--target-source", "follower_list", 
            "--target-details", '{"account_to_scrape": "target_account"}', 
            "--message-templates", '[{"template": "Hello {{name}}"}]'
        ]
        self.run_test(args)
        
        # Verify the method was called with correct arguments
        self.mock_tool.create_messaging_campaign.assert_called_once_with(
            account_ids=["acc_123", "acc_456"], 
            target_source="follower_list", 
            target_details={"account_to_scrape": "target_account"}, 
            message_templates=[{"template": "Hello {{name}}"}],
            use_cupidbot=False
        )
        logger.info("✅ message create-campaign command test passed")
    
    def test_message_start_campaign(self):
        """Test the message start-campaign command."""
        args = ["message", "start-campaign", "--campaign-id", "camp_123"]
        self.run_test(args)
        
        # Verify the method was called with correct arguments
        self.mock_tool.agency.get_agent.assert_called_with("MessagingAgent")
        self.mock_tool.agency.get_agent("MessagingAgent").start_campaign.assert_called_once_with(
            campaign_id="camp_123",
            start_time=None
        )
        logger.info("✅ message start-campaign command test passed")
    
    def test_post_create(self):
        """Test the post create command."""
        args = [
            "post", "create", 
            "--account-id", "acc_123", 
            "--media-paths", "img1.jpg,img2.jpg", 
            "--caption", "Test caption", 
            "--hashtags", "test,instagram"
        ]
        self.run_test(args)
        
        # Verify the method was called with correct arguments
        self.mock_tool.create_post.assert_called_once_with(
            account_id="acc_123", 
            media_paths=["img1.jpg", "img2.jpg"], 
            caption="Test caption", 
            hashtags=["test", "instagram"], 
            tagged_users=[], 
            location="", 
            scheduled_time=None
        )
        logger.info("✅ post create command test passed")
    
    def test_run(self):
        """Test the run command."""
        args = ["run"]
        self.run_test(args)
        
        # Verify the method was called
        self.mock_tool.run.assert_called_once()
        logger.info("✅ run command test passed")
    
    def test_missing_subcommand(self):
        """Test behavior when a command is provided without a subcommand."""
        args = ["account"]
        try:
            self.run_test(args)
            logger.error("❌ Missing subcommand test failed - should have raised an error")
        except SystemExit:
            logger.info("✅ Missing subcommand test passed - correctly raised SystemExit")
    
    def test_invalid_command(self):
        """Test behavior with an invalid command."""
        args = ["invalid_command"]
        try:
            self.run_test(args)
            logger.error("❌ Invalid command test failed - should have raised an error")
        except SystemExit:
            logger.info("✅ Invalid command test passed - correctly raised SystemExit")
    
    def run_test(self, args):
        """Run a test with the given arguments."""
        # Import the necessary functions from run.py
        from run import parse_arguments, main, process_account_commands, process_message_commands, process_post_commands, run_tool
        
        # Mock sys.argv
        with patch('sys.argv', ['run.py'] + args):
            # Mock the InstagramAutomationTool class
            with patch('run.InstagramAutomationTool', return_value=self.mock_tool):
                # Call the main function
                try:
                    main()
                except SystemExit as e:
                    # Re-raise SystemExit for tests that expect it
                    raise e
    
    def run_all_tests(self):
        """Run all tests."""
        logger.info("Starting CLI tests...")
        
        try:
            self.test_account_create()
            self.test_account_setup_profile()
            self.test_account_health()
            self.test_message_create_campaign()
            self.test_message_start_campaign()
            self.test_post_create()
            self.test_run()
            self.test_missing_subcommand()
            self.test_invalid_command()
            
            logger.info("All tests completed successfully! ✅")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

if __name__ == "__main__":
    test_cli = TestCLI()
    test_cli.run_all_tests()