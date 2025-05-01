"""
Database
--------
Utility for storing and retrieving data for the Instagram Automation Tool.
Supports JSON file-based storage by default, with extensibility for other database types.
"""

import os
import json
import logging
import time
from typing import Dict, Any, List, Optional, Union

logger = logging.getLogger(__name__)

class Database:
    """Database class for storing and retrieving data."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the database.
        
        Args:
            config: Database configuration
        """
        self.config = config
        self.db_type = config.get("type", "json")
        self.db_path = config.get("path", "data/database.json")
        
        # Initialize database
        self._initialize_database()
        
        logger.info(f"Database initialized: {self.db_type} at {self.db_path}")
    
    def _initialize_database(self) -> None:
        """Initialize the database based on the configured type."""
        if self.db_type == "json":
            self._initialize_json_database()
        else:
            logger.error(f"Unsupported database type: {self.db_type}")
            logger.info("Falling back to JSON database")
            self.db_type = "json"
            self.db_path = "data/database.json"
            self._initialize_json_database()
    
    def _initialize_json_database(self) -> None:
        """Initialize a JSON file-based database."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        
        # Create database file if it doesn't exist
        if not os.path.exists(self.db_path):
            logger.info(f"Creating new database file: {self.db_path}")
            self._save_json_data({
                "accounts": [],
                "campaigns": [],
                "posts": [],
                "browser_profiles": [],
                "metadata": {
                    "created_at": time.time(),
                    "version": "1.0.0"
                }
            })
    
    def _load_json_data(self) -> Dict[str, Any]:
        """Load data from JSON database.
        
        Returns:
            Dict containing database data
        """
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.error(f"Error loading database file: {self.db_path}")
            return {
                "accounts": [],
                "campaigns": [],
                "posts": [],
                "browser_profiles": [],
                "metadata": {
                    "created_at": time.time(),
                    "version": "1.0.0"
                }
            }
    
    def _save_json_data(self, data: Dict[str, Any]) -> None:
        """Save data to JSON database.
        
        Args:
            data: Data to save
        """
        try:
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving database: {str(e)}")
    
    def get_all(self, collection: str) -> List[Dict[str, Any]]:
        """Get all items from a collection.
        
        Args:
            collection: Name of the collection
            
        Returns:
            List of items in the collection
        """
        if self.db_type == "json":
            data = self._load_json_data()
            return data.get(collection, [])
        
        return []
    
    def get_by_id(self, collection: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Get an item by ID from a collection.
        
        Args:
            collection: Name of the collection
            item_id: ID of the item
            
        Returns:
            Item if found, None otherwise
        """
        items = self.get_all(collection)
        
        for item in items:
            if item.get("id") == item_id:
                return item
        
        return None
    
    def insert(self, collection: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """Insert an item into a collection.
        
        Args:
            collection: Name of the collection
            item: Item to insert
            
        Returns:
            Inserted item
        """
        if self.db_type == "json":
            data = self._load_json_data()
            
            # Ensure collection exists
            if collection not in data:
                data[collection] = []
            
            # Add item to collection
            data[collection].append(item)
            
            # Save data
            self._save_json_data(data)
            
            return item
        
        return item
    
    def update(self, collection: str, item_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an item in a collection.
        
        Args:
            collection: Name of the collection
            item_id: ID of the item to update
            updates: Updates to apply
            
        Returns:
            Updated item if found, None otherwise
        """
        if self.db_type == "json":
            data = self._load_json_data()
            
            # Ensure collection exists
            if collection not in data:
                return None
            
            # Find and update item
            for i, item in enumerate(data[collection]):
                if item.get("id") == item_id:
                    # Apply updates
                    for key, value in updates.items():
                        item[key] = value
                    
                    # Save data
                    self._save_json_data(data)
                    
                    return item
            
            return None
        
        return None
    
    def delete(self, collection: str, item_id: str) -> bool:
        """Delete an item from a collection.
        
        Args:
            collection: Name of the collection
            item_id: ID of the item to delete
            
        Returns:
            True if item was deleted, False otherwise
        """
        if self.db_type == "json":
            data = self._load_json_data()
            
            # Ensure collection exists
            if collection not in data:
                return False
            
            # Find and delete item
            for i, item in enumerate(data[collection]):
                if item.get("id") == item_id:
                    # Remove item
                    data[collection].pop(i)
                    
                    # Save data
                    self._save_json_data(data)
                    
                    return True
            
            return False
        
        return False
    
    def query(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query items in a collection.
        
        Args:
            collection: Name of the collection
            query: Query parameters
            
        Returns:
            List of items matching the query
        """
        items = self.get_all(collection)
        results = []
        
        for item in items:
            match = True
            
            # Check if item matches all query parameters
            for key, value in query.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            
            if match:
                results.append(item)
        
        return results