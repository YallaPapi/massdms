"""
Config Loader
------------
Utility for loading and validating configuration files.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict containing configuration
    """
    logger.info(f"Loading configuration from: {config_path}")
    
    # Check if config file exists
    if not os.path.exists(config_path):
        logger.warning(f"Configuration file not found: {config_path}")
        logger.info("Creating default configuration")
        config = create_default_config()
        save_config(config, config_path)
        return config
    
    # Load config file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Validate config
        validate_config(config)
        
        logger.info(f"Configuration loaded successfully from: {config_path}")
        return config
    
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in configuration file: {config_path}")
        logger.info("Creating default configuration")
        config = create_default_config()
        save_config(config, config_path)
        return config
    
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        logger.info("Creating default configuration")
        config = create_default_config()
        save_config(config, config_path)
        return config

def create_default_config() -> Dict[str, Any]:
    """Create a default configuration.
    
    Returns:
        Dict containing default configuration
    """
    default_config = {
        "database": {
            "type": "json",
            "path": "data/database.json"
        },
        "adspower": {
            "api_url": "http://localhost:50325",
            "group_id": "0"
        },
        "verification": {
            "daisysms": {
                "api_key": "",
                "service": "instagram"
            },
            "email": {
                "provider": "temp_mail"
            }
        },
        "cupidbot": {
            "enabled": True,
            "default_personality": "friendly",
            "default_response_style": "casual"
        },
        "accounts": [],
        "campaigns": [],
        "posts": [],
        "logging": {
            "level": "INFO",
            "file": "instagram_automation.log"
        }
    }
    
    return default_config

def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to a JSON file.
    
    Args:
        config: Configuration to save
        config_path: Path to save the configuration to
    """
    logger.info(f"Saving configuration to: {config_path}")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(config_path)), exist_ok=True)
    
    # Save config file
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Configuration saved successfully to: {config_path}")
    
    except Exception as e:
        logger.error(f"Error saving configuration: {str(e)}")

def validate_config(config: Dict[str, Any]) -> None:
    """Validate configuration structure.
    
    Args:
        config: Configuration to validate
        
    Raises:
        ValueError: If configuration is invalid
    """
    # Check required top-level keys
    required_keys = ["database", "adspower"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    # Validate database configuration
    if "type" not in config["database"]:
        raise ValueError("Missing database type in configuration")
    
    # Validate AdsPower configuration
    if "api_url" not in config["adspower"]:
        raise ValueError("Missing AdsPower API URL in configuration")