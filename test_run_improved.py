#!/usr/bin/env python3
"""
Comprehensive Test Script for Improved Instagram Automation Tool CLI
------------------------------------------------------------------
This script tests the improved command-line interface of the Instagram Automation Tool
by mocking the InstagramAutomationTool class and its methods.
"""

import sys
import logging
import subprocess
import json
from unittest.mock import MagicMock, patch
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestImprovedCLI:
    """Test class for the improved Instagram Automation Tool CLI."""
    
    def __init__(self):
        """Initialize the test class."""
        self.mock_tool = MagicMock()
        self.setup_mock_methods()
    
    def setup_mock_methods(self):
        """Set up mock methods for the InstagramAutomationTool class."""
        # Account methods
        self.mock_tool.create_account.return_value = {"id": "acc_123", "status": "success"}
        self.mock_tool.setup_profile.return_value = {"account_id": "acc_123", "status": "success"}
        self.mock_tool.check_account_health.return_value = {
            "account_id": "acc_123", 
            "health": {"status": "healthy"}
        }
        
        # Message methods
        self.mock_tool.create_messaging_campaign.return_value = {"id": "camp_123", "status": "success"}
        self.mock_tool.start_campaign.return_value = {"campaign_id": "camp_123", "status": "active"}
        self.mock_tool.send_message.return_value = {"message_sent": True, "status": "success"}
        
        # Post methods
        self.mock_tool.create_post.return_value = {"id": "post_123", "status": "success"}
        self.mock_tool.publish_post.return_value = {"post_id": "post_123", "status": "published"}
        self.mock_tool.track_post_performance.return_value = {
            "post_id": "post_123", 
            "performance": {"likes": 42, "comments": 7},
            "status": "success"
        }
        
        # Run method
        self.mock_tool.run.return_value = None
    
    def test_no_command(self):
        """Test behavior when no command is provided."""
        logger.info("Testing no command...")
        with patch('sys.argv', ['run_improved.py']):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    logger.error("❌ No command test failed - should have exited")
                    return False
                except SystemExit as e:
                    if e.code != 0:
                        logger.info("✅ No command test passed - correctly exited with non-zero code")
                        return True
                    else:
                        logger.error("❌ No command test failed - exited with zero code")
                        return False
    
    def test_missing_subcommand(self):
        """Test behavior when a command is provided without a subcommand."""
        logger.info("Testing missing subcommand...")
        commands = ["account", "message", "post"]
        all_passed = True
        
        for cmd in commands:
            with patch('sys.argv', ['run_improved.py', cmd]):
                with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                    try:
                        from run_improved import main
                        main()
                        logger.error(f"❌ Missing subcommand test for '{cmd}' failed - should have exited")
                        all_passed = False
                    except SystemExit as e:
                        if e.code != 0:
                            logger.info(f"✅ Missing subcommand test for '{cmd}' passed - correctly exited with non-zero code")
                        else:
                            logger.error(f"❌ Missing subcommand test for '{cmd}' failed - exited with zero code")
                            all_passed = False
        
        return all_passed
    
    def test_invalid_command(self):
        """Test behavior with an invalid command."""
        logger.info("Testing invalid command...")
        with patch('sys.argv', ['run_improved.py', 'invalid_command']):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    logger.error("❌ Invalid command test failed - should have exited")
                    return False
                except SystemExit as e:
                    if e.code != 0:
                        logger.info("✅ Invalid command test passed - correctly exited with non-zero code")
                        return True
                    else:
                        logger.error("❌ Invalid command test failed - exited with zero code")
                        return False
    
    def test_invalid_subcommand(self):
        """Test behavior with an invalid subcommand."""
        logger.info("Testing invalid subcommand...")
        commands = [
            ["account", "invalid_subcommand"],
            ["message", "invalid_subcommand"],
            ["post", "invalid_subcommand"]
        ]
        all_passed = True
        
        for cmd in commands:
            with patch('sys.argv', ['run_improved.py'] + cmd):
                with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                    try:
                        from run_improved import main
                        main()
                        logger.error(f"❌ Invalid subcommand test for '{cmd[0]} {cmd[1]}' failed - should have exited")
                        all_passed = False
                    except SystemExit as e:
                        if e.code != 0:
                            logger.info(f"✅ Invalid subcommand test for '{cmd[0]} {cmd[1]}' passed - correctly exited with non-zero code")
                        else:
                            logger.error(f"❌ Invalid subcommand test for '{cmd[0]} {cmd[1]}' failed - exited with zero code")
                            all_passed = False
        
        return all_passed
    
    def test_account_create(self):
        """Test the account create command."""
        logger.info("Testing account create command...")
        with patch('sys.argv', [
            'run_improved.py', 'account', 'create', 
            '--username', 'test_user', 
            '--password', 'test_pass', 
            '--email', 'test@example.com'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.create_account.assert_called_once_with(
                        username='test_user', 
                        password='test_pass', 
                        email='test@example.com', 
                        phone=None
                    )
                    logger.info("✅ account create command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ account create command test failed: {str(e)}")
                    return False
    
    def test_account_setup_profile(self):
        """Test the account setup-profile command."""
        logger.info("Testing account setup-profile command...")
        with patch('sys.argv', [
            'run_improved.py', 'account', 'setup-profile', 
            '--account-id', 'acc_123', 
            '--bio', 'Test bio', 
            '--profile-pic', 'pic.jpg'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.setup_profile.assert_called_once_with(
                        account_id='acc_123', 
                        bio='Test bio', 
                        profile_pic='pic.jpg', 
                        external_link=''
                    )
                    logger.info("✅ account setup-profile command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ account setup-profile command test failed: {str(e)}")
                    return False
    
    def test_account_health(self):
        """Test the account health command."""
        logger.info("Testing account health command...")
        with patch('sys.argv', [
            'run_improved.py', 'account', 'health', 
            '--account-id', 'acc_123'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.check_account_health.assert_called_once_with(
                        account_id='acc_123'
                    )
                    logger.info("✅ account health command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ account health command test failed: {str(e)}")
                    return False
    
    def test_message_create_campaign(self):
        """Test the message create-campaign command."""
        logger.info("Testing message create-campaign command...")
        with patch('sys.argv', [
            'run_improved.py', 'message', 'create-campaign', 
            '--account-ids', 'acc_123,acc_456', 
            '--target-source', 'follower_list', 
            '--target-details', '{"account_to_scrape": "target_account"}', 
            '--message-templates', '[{"template": "Hello {{name}}"}]'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.create_messaging_campaign.assert_called_once_with(
                        account_ids=['acc_123', 'acc_456'], 
                        target_source='follower_list', 
                        target_details={"account_to_scrape": "target_account"}, 
                        message_templates=[{"template": "Hello {{name}}"}],
                        use_cupidbot=False
                    )
                    logger.info("✅ message create-campaign command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ message create-campaign command test failed: {str(e)}")
                    return False
    
    def test_message_start_campaign(self):
        """Test the message start-campaign command."""
        logger.info("Testing message start-campaign command...")
        with patch('sys.argv', [
            'run_improved.py', 'message', 'start-campaign', 
            '--campaign-id', 'camp_123'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.start_campaign.assert_called_once_with(
                        campaign_id='camp_123',
                        start_time=None
                    )
                    logger.info("✅ message start-campaign command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ message start-campaign command test failed: {str(e)}")
                    return False
    
    def test_message_send(self):
        """Test the message send command."""
        logger.info("Testing message send command...")
        with patch('sys.argv', [
            'run_improved.py', 'message', 'send', 
            '--account-id', 'acc_123', 
            '--target-username', 'target_user', 
            '--message-template', '{"template": "Hello {{name}}"}'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.send_message.assert_called_once_with(
                        account_id='acc_123',
                        target_username='target_user',
                        message_template={"template": "Hello {{name}}"},
                        use_cupidbot=False
                    )
                    logger.info("✅ message send command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ message send command test failed: {str(e)}")
                    return False
    
    def test_post_create(self):
        """Test the post create command."""
        logger.info("Testing post create command...")
        with patch('sys.argv', [
            'run_improved.py', 'post', 'create', 
            '--account-id', 'acc_123', 
            '--media-paths', 'img1.jpg,img2.jpg', 
            '--caption', 'Test caption', 
            '--hashtags', 'test,instagram'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.create_post.assert_called_once_with(
                        account_id='acc_123', 
                        media_paths=['img1.jpg', 'img2.jpg'], 
                        caption='Test caption', 
                        hashtags=['test', 'instagram'], 
                        tagged_users=[], 
                        location='', 
                        scheduled_time=None
                    )
                    logger.info("✅ post create command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ post create command test failed: {str(e)}")
                    return False
    
    def test_post_publish(self):
        """Test the post publish command."""
        logger.info("Testing post publish command...")
        with patch('sys.argv', [
            'run_improved.py', 'post', 'publish', 
            '--post-id', 'post_123'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.publish_post.assert_called_once_with(
                        post_id='post_123'
                    )
                    logger.info("✅ post publish command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ post publish command test failed: {str(e)}")
                    return False
    
    def test_post_track(self):
        """Test the post track command."""
        logger.info("Testing post track command...")
        with patch('sys.argv', [
            'run_improved.py', 'post', 'track', 
            '--post-id', 'post_123'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called with correct arguments
                    self.mock_tool.track_post_performance.assert_called_once_with(
                        post_id='post_123'
                    )
                    logger.info("✅ post track command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ post track command test failed: {str(e)}")
                    return False
    
    def test_run(self):
        """Test the run command."""
        logger.info("Testing run command...")
        with patch('sys.argv', ['run_improved.py', 'run']):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    
                    # Verify the method was called
                    self.mock_tool.run.assert_called_once()
                    logger.info("✅ run command test passed")
                    return True
                except Exception as e:
                    logger.error(f"❌ run command test failed: {str(e)}")
                    return False
    
    def test_error_handling(self):
        """Test error handling in the CLI."""
        logger.info("Testing error handling...")
        
        # Test error handling for account create
        self.mock_tool.create_account.return_value = {"status": "error", "message": "Failed to create account"}
        
        with patch('sys.argv', [
            'run_improved.py', 'account', 'create', 
            '--username', 'test_user', 
            '--password', 'test_pass', 
            '--email', 'test@example.com'
        ]):
            with patch('run_improved.InstagramAutomationTool', return_value=self.mock_tool):
                try:
                    from run_improved import main
                    main()
                    logger.error("❌ Error handling test failed - should have exited")
                    return False
                except SystemExit as e:
                    if e.code != 0:
                        logger.info("✅ Error handling test passed - correctly exited with non-zero code")
                        return True
                    else:
                        logger.error("❌ Error handling test failed - exited with zero code")
                        return False
    
    def run_all_tests(self):
        """Run all tests."""
        logger.info("Starting CLI tests for improved run.py...")
        
        tests = [
            self.test_no_command,
            self.test_missing_subcommand,
            self.test_invalid_command,
            self.test_invalid_subcommand,
            self.test_account_create,
            self.test_account_setup_profile,
            self.test_account_health,
            self.test_message_create_campaign,
            self.test_message_start_campaign,
            self.test_message_send,
            self.test_post_create,
            self.test_post_publish,
            self.test_post_track,
            self.test_run,
            self.test_error_handling
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Error running test {test.__name__}: {str(e)}")
                failed += 1
        
        logger.info(f"Tests completed: {passed} passed, {failed} failed")
        
        if failed == 0:
            logger.info("All tests passed! ✅")
        else:
            logger.error(f"{failed} tests failed ❌")

if __name__ == "__main__":
    test_cli = TestImprovedCLI()
    test_cli.run_all_tests()