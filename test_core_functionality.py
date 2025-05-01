#!/usr/bin/env python3
"""
Test Core Functionality of Instagram Automation Tool
---------------------------------------------------
This script tests the core functionality of the Instagram Automation Tool,
including importing, initialization, configuration loading, database handling,
and agency setup.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_core_functionality.log')
    ]
)
logger = logging.getLogger(__name__)

def test_agency_swarm_availability():
    """Test if agency-swarm is available or create a mock implementation."""
    logger.info("Testing agency-swarm availability...")
    
    try:
        import agency_swarm
        logger.info(f"agency-swarm is available (version: {getattr(agency_swarm, '__version__', 'unknown')})")
        return True
    except ImportError:
        logger.warning("agency-swarm is not available")
        
        # Check if mock_agency_swarm exists
        if os.path.exists("mock_agency_swarm"):
            logger.info("mock_agency_swarm directory exists")
            
            # Try to install mock_agency_swarm
            try:
                import subprocess
                logger.info("Installing mock agency-swarm...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "mock_agency_swarm"])
                logger.info("Mock agency-swarm installed successfully!")
                
                # Verify installation
                import agency_swarm
                logger.info("Mock agency-swarm imported successfully!")
                return True
            except Exception as e:
                logger.error(f"Error installing mock agency-swarm: {e}")
                return False
        else:
            # Create mock_agency_swarm
            logger.info("Creating mock agency-swarm...")
            try:
                import create_mock_agency_swarm
                create_mock_agency_swarm.create_mock_agency_swarm()
                
                # Verify installation
                import agency_swarm
                logger.info("Mock agency-swarm created and imported successfully!")
                return True
            except Exception as e:
                logger.error(f"Error creating mock agency-swarm: {e}")
                return False

def test_import_and_initialization():
    """Test importing and initializing the Instagram Automation Tool."""
    logger.info("Testing import and initialization...")
    
    try:
        # Test importing the tool
        from instagram_automation_tool import InstagramAutomationTool
        logger.info("Import successful")
        
        # Test initializing the tool
        tool = InstagramAutomationTool()
        logger.info("Initialization successful")
        
        return tool
    except Exception as e:
        logger.error(f"Error importing or initializing tool: {e}")
        return None

def test_config_loading(tool):
    """Test configuration loading from config.json."""
    logger.info("Testing configuration loading...")
    
    if not tool:
        logger.error("Tool not initialized")
        return False
    
    try:
        # Check if config is loaded
        if not tool.config:
            logger.error("Configuration not loaded")
            return False
        
        # Check required config keys
        required_keys = ["database", "adspower"]
        for key in required_keys:
            if key not in tool.config:
                logger.error(f"Missing required configuration key: {key}")
                return False
        
        logger.info("Configuration loaded successfully")
        logger.info(f"Database type: {tool.config.get('database', {}).get('type', 'unknown')}")
        logger.info(f"AdsPower API URL: {tool.config.get('adspower', {}).get('api_url', 'unknown')}")
        
        return True
    except Exception as e:
        logger.error(f"Error testing configuration loading: {e}")
        return False

def test_database_handling(tool):
    """Test database handling from database.json."""
    logger.info("Testing database handling...")
    
    if not tool:
        logger.error("Tool not initialized")
        return False
    
    try:
        # Check if database is initialized
        if not tool.db:
            logger.error("Database not initialized")
            return False
        
        # Check database type and path
        logger.info(f"Database type: {tool.db.db_type}")
        logger.info(f"Database path: {tool.db.db_path}")
        
        # Verify database path matches config
        expected_path = "data/database.json"
        if tool.db.db_path != expected_path:
            logger.error(f"Database path mismatch: expected '{expected_path}', got '{tool.db.db_path}'")
            return False
        
        # Test database operations
        # 1. Get all accounts
        accounts = tool.db.get_all("accounts")
        logger.info(f"Found {len(accounts)} accounts")
        
        # 2. Insert a test account
        test_account = {
            "id": f"test_{int(datetime.now().timestamp())}",
            "username": "test_user",
            "email": "test@example.com",
            "created_at": datetime.now().timestamp()
        }
        inserted_account = tool.db.insert("accounts", test_account)
        logger.info(f"Inserted test account: {inserted_account['id']}")
        
        # 3. Get the test account
        accounts_after_insert = tool.db.get_all("accounts")
        logger.info(f"Found {len(accounts_after_insert)} accounts after insert")
        
        # 4. Delete the test account
        deleted = tool.db.delete("accounts", test_account["id"])
        logger.info(f"Deleted test account: {deleted}")
        
        # 5. Verify deletion
        accounts_after_delete = tool.db.get_all("accounts")
        logger.info(f"Found {len(accounts_after_delete)} accounts after delete")
        
        # Check if operations were successful
        if len(accounts_after_insert) != len(accounts) + 1:
            logger.error("Insert operation failed")
            return False
        
        if len(accounts_after_delete) != len(accounts):
            logger.error("Delete operation failed")
            return False
        
        logger.info("Database operations successful")
        return True
    except Exception as e:
        logger.error(f"Error testing database handling: {e}")
        return False

def test_agency_setup(tool):
    """Test agency setup with all agents."""
    logger.info("Testing agency setup...")
    
    if not tool:
        logger.error("Tool not initialized")
        return False
    
    try:
        # Check if agency is initialized
        if not tool.agency:
            logger.error("Agency not initialized")
            return False
        
        # Check if all required agents are present
        required_agents = [
            "AccountManagerAgent",
            "MessagingAgent",
            "ContentPosterAgent",
            "BrowserManagerAgent"
        ]
        
        for agent_name in required_agents:
            agent = tool.agency.get_agent(agent_name)
            if not agent:
                logger.error(f"Agent not found: {agent_name}")
                return False
            logger.info(f"Agent found: {agent_name}")
        
        logger.info("All required agents are present")
        
        # Test agent functionality (basic)
        account_manager = tool.agency.get_agent("AccountManagerAgent")
        browser_manager = tool.agency.get_agent("BrowserManagerAgent")
        
        # Test creating a browser profile
        profile = browser_manager.create_browser_profile("test_profile")
        logger.info(f"Created browser profile: {profile['profile_id']}")
        
        # Test creating an account
        account = account_manager.create_account(
            username="test_user",
            password="test_password",
            email="test@example.com"
        )
        logger.info(f"Created account: {account['id']}")
        
        logger.info("Agency setup and basic functionality tests successful")
        return True
    except Exception as e:
        logger.error(f"Error testing agency setup: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("Starting core functionality tests...")
    
    # Test agency-swarm availability
    agency_swarm_available = test_agency_swarm_availability()
    if not agency_swarm_available:
        logger.error("agency-swarm is not available and could not be created")
        return False
    
    # Test import and initialization
    tool = test_import_and_initialization()
    if not tool:
        logger.error("Import and initialization failed")
        return False
    
    # Test configuration loading
    config_loading_success = test_config_loading(tool)
    if not config_loading_success:
        logger.error("Configuration loading failed")
        return False
    
    # Test database handling
    database_handling_success = test_database_handling(tool)
    if not database_handling_success:
        logger.error("Database handling failed")
        return False
    
    # Test agency setup
    agency_setup_success = test_agency_setup(tool)
    if not agency_setup_success:
        logger.error("Agency setup failed")
        return False
    
    logger.info("All core functionality tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)