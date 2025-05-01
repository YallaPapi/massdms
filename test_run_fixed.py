#!/usr/bin/env python3
"""
Test Script for Fixed Instagram Automation Tool CLI
-------------------------------------------------
This script tests the fixed version of the Instagram Automation Tool CLI.
"""

import sys
import logging
import subprocess
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command):
    """Run a command and return the output."""
    logger.info(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        logger.error(f"Error running command: {str(e)}")
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e)
        }

def test_no_command():
    """Test behavior when no command is provided."""
    result = run_command(["python", "run_fixed.py"])
    if result["returncode"] != 0:
        logger.info("✅ No command test passed - correctly exited with non-zero code")
    else:
        logger.error("❌ No command test failed - should have exited with non-zero code")
    return result["returncode"] != 0

def test_missing_subcommand():
    """Test behavior when a command is provided without a subcommand."""
    commands = ["account", "message", "post"]
    all_passed = True
    
    for cmd in commands:
        result = run_command(["python", "run_fixed.py", cmd])
        if result["returncode"] != 0:
            logger.info(f"✅ Missing subcommand test for '{cmd}' passed - correctly exited with non-zero code")
        else:
            logger.error(f"❌ Missing subcommand test for '{cmd}' failed - should have exited with non-zero code")
            all_passed = False
    
    return all_passed

def test_invalid_command():
    """Test behavior with an invalid command."""
    result = run_command(["python", "run_fixed.py", "invalid_command"])
    if result["returncode"] != 0:
        logger.info("✅ Invalid command test passed - correctly exited with non-zero code")
    else:
        logger.error("❌ Invalid command test failed - should have exited with non-zero code")
    return result["returncode"] != 0

def test_invalid_subcommand():
    """Test behavior with an invalid subcommand."""
    commands = [
        ["account", "invalid_subcommand"],
        ["message", "invalid_subcommand"],
        ["post", "invalid_subcommand"]
    ]
    all_passed = True
    
    for cmd in commands:
        result = run_command(["python", "run_fixed.py"] + cmd)
        if result["returncode"] != 0:
            logger.info(f"✅ Invalid subcommand test for '{cmd[0]} {cmd[1]}' passed - correctly exited with non-zero code")
        else:
            logger.error(f"❌ Invalid subcommand test for '{cmd[0]} {cmd[1]}' failed - should have exited with non-zero code")
            all_passed = False
    
    return all_passed

def test_account_create():
    """Test the account create command."""
    # This will fail because we're not actually running the tool, but we're testing the argument parsing
    result = run_command([
        "python", "run_fixed.py", "account", "create", 
        "--username", "test_user", 
        "--password", "test_pass", 
        "--email", "test@example.com"
    ])
    
    # We expect this to fail when actually running, but the argument parsing should work
    logger.info(f"Account create command output: {result['stderr']}")
    return "argument parsing" in result["stderr"].lower() or "instagram" in result["stderr"].lower()

def test_message_create_campaign():
    """Test the message create-campaign command."""
    # This will fail because we're not actually running the tool, but we're testing the argument parsing
    result = run_command([
        "python", "run_fixed.py", "message", "create-campaign", 
        "--account-ids", "acc_123,acc_456", 
        "--target-source", "follower_list", 
        "--target-details", '{"account_to_scrape": "target_account"}', 
        "--message-templates", '[{"template": "Hello {{name}}"}]'
    ])
    
    # We expect this to fail when actually running, but the argument parsing should work
    logger.info(f"Message create-campaign command output: {result['stderr']}")
    return "argument parsing" in result["stderr"].lower() or "instagram" in result["stderr"].lower()

def test_post_create():
    """Test the post create command."""
    # This will fail because we're not actually running the tool, but we're testing the argument parsing
    result = run_command([
        "python", "run_fixed.py", "post", "create", 
        "--account-id", "acc_123", 
        "--media-paths", "img1.jpg,img2.jpg", 
        "--caption", "Test caption", 
        "--hashtags", "test,instagram"
    ])
    
    # We expect this to fail when actually running, but the argument parsing should work
    logger.info(f"Post create command output: {result['stderr']}")
    return "argument parsing" in result["stderr"].lower() or "instagram" in result["stderr"].lower()

def test_json_error_handling():
    """Test JSON error handling in message create-campaign command."""
    result = run_command([
        "python", "run_fixed.py", "message", "create-campaign", 
        "--account-ids", "acc_123,acc_456", 
        "--target-source", "follower_list", 
        "--target-details", '{invalid_json}', 
        "--message-templates", '[{"template": "Hello {{name}}"}]'
    ])
    
    if result["returncode"] != 0 and "error parsing json" in result["stderr"].lower():
        logger.info("✅ JSON error handling test passed - correctly detected invalid JSON")
        return True
    else:
        logger.error("❌ JSON error handling test failed - should have detected invalid JSON")
        return False

def test_datetime_error_handling():
    """Test datetime error handling in post create command."""
    result = run_command([
        "python", "run_fixed.py", "post", "create", 
        "--account-id", "acc_123", 
        "--media-paths", "img1.jpg,img2.jpg", 
        "--caption", "Test caption", 
        "--scheduled-time", "invalid-datetime"
    ])
    
    if result["returncode"] != 0 and "invalid datetime format" in result["stderr"].lower():
        logger.info("✅ Datetime error handling test passed - correctly detected invalid datetime")
        return True
    else:
        logger.error("❌ Datetime error handling test failed - should have detected invalid datetime")
        return False

def run_all_tests():
    """Run all tests."""
    logger.info("Starting CLI tests for fixed run.py...")
    
    tests = [
        test_no_command,
        test_missing_subcommand,
        test_invalid_command,
        test_invalid_subcommand,
        test_account_create,
        test_message_create_campaign,
        test_post_create,
        test_json_error_handling,
        test_datetime_error_handling
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
    run_all_tests()