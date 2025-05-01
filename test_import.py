#!/usr/bin/env python3
"""
Test script to verify if all required dependencies are installed
and if the Instagram Automation Tool can be imported and initialized correctly.
"""

import sys
import json
import os

def test_imports():
    """Test importing all required packages."""
    missing_packages = []
    
    # Test essential packages
    essential_packages = [
        "requests",
        "dotenv",
        "pydantic",
        "selenium",
        "webdriver_manager",
        "tqdm",
        "colorama"
    ]
    
    print("Testing essential packages:")
    for package in essential_packages:
        try:
            if package == "dotenv":
                # python-dotenv is imported as dotenv
                __import__("dotenv")
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ✗ {package}")
    
    # Test agency-swarm
    print("\nTesting agency-swarm:")
    try:
        import agency_swarm
        print("  ✓ agency_swarm")
        print(f"    Version: {getattr(agency_swarm, '__version__', 'unknown')}")
        print(f"    Path: {agency_swarm.__file__}")
    except ImportError:
        missing_packages.append("agency_swarm")
        print("  ✗ agency_swarm")
    
    # Report results
    if missing_packages:
        print("\nMissing packages:")
        for package in missing_packages:
            print(f"  - {package}")
        return False
    else:
        print("\nAll required packages are installed!")
        return True

def test_instagram_automation_tool():
    """Test importing and initializing the Instagram Automation Tool."""
    print("\nTesting Instagram Automation Tool:")
    
    try:
        # Test importing the tool
        print("  Testing import...")
        from instagram_automation_tool import InstagramAutomationTool
        print("  ✓ Import successful")
        
        # Test initializing the tool
        print("  Testing initialization...")
        tool = InstagramAutomationTool()
        print("  ✓ Initialization successful")
        
        # Test if agency setup works correctly
        print("  Testing agency setup...")
        agency = tool.agency
        
        # Check if all required agents are present
        required_agents = [
            "AccountManagerAgent",
            "MessagingAgent",
            "ContentPosterAgent",
            "BrowserManagerAgent"
        ]
        
        for agent_name in required_agents:
            agent = agency.get_agent(agent_name)
            if agent:
                print(f"  ✓ Agent found: {agent_name}")
            else:
                print(f"  ✗ Agent not found: {agent_name}")
                return False
        
        # Test configuration loading
        print("\nTesting configuration loading:")
        if tool.config:
            print(f"  ✓ Configuration loaded successfully")
            print(f"    Database type: {tool.config.get('database', {}).get('type', 'unknown')}")
        else:
            print(f"  ✗ Configuration loading failed")
            return False
        
        # Test database initialization
        print("\nTesting database initialization:")
        if tool.db:
            print(f"  ✓ Database initialized successfully")
            print(f"    Database path: {tool.db.db_path}")
            
            # Verify database path
            expected_path = "data/database.json"
            if tool.db.db_path != expected_path:
                print(f"  ✗ Database path mismatch: expected '{expected_path}', got '{tool.db.db_path}'")
                return False
            else:
                print(f"  ✓ Database path is correct: {tool.db.db_path}")
        else:
            print(f"  ✗ Database initialization failed")
            return False
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    imports_success = test_imports()
    
    if imports_success:
        tool_success = test_instagram_automation_tool()
        success = imports_success and tool_success
    else:
        success = False
    
    sys.exit(0 if success else 1)
