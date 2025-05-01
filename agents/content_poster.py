"""
Content Poster Agent
------------------
Responsible for creating and posting content to Instagram accounts, including:
- Post creation with media, captions, and hashtags
- Post scheduling
- Performance tracking
"""

import logging
import time
import random
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import from main module instead of agency_swarm
from instagram_automation_tool import Agent, Task

logger = logging.getLogger(__name__)

class ContentPosterAgent(Agent):
    """Agent responsible for creating and posting Instagram content."""
    
    def __init__(self):
        """Initialize the Content Poster Agent."""
        super().__init__(
            name="ContentPosterAgent",
            description="Creates and posts content to Instagram accounts",
            instructions="""
            You are responsible for creating and posting content to Instagram accounts.
            Your tasks include:
            1. Creating posts with media, captions, and hashtags
            2. Scheduling posts for optimal times
            3. Tracking post performance
            
            Always ensure content appears authentic and follows best practices.
            Use proper hashtags and captions to maximize engagement.
            """
        )
    
    @Task
    def create_post(self, account_id: str, media_paths: List[str], caption: str,
                   hashtags: List[str] = [], tagged_users: List[str] = [],
                   location: str = "", scheduled_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Create and schedule a post.
        
        Args:
            account_id: ID of the account to post from
            media_paths: Paths to media files (images/videos)
            caption: Post caption
            hashtags: List of hashtags
            tagged_users: List of users to tag
            location: Location tag
            scheduled_time: When to publish the post
            
        Returns:
            Dict containing post information
        """
        logger.info(f"Creating post for account: {account_id}")
        
        # Validate media files
        valid_media = self._validate_media(media_paths)
        if not valid_media:
            logger.error("No valid media files provided")
            return {"status": "error", "message": "No valid media files provided"}
        
        # Format caption with hashtags
        formatted_caption = caption
        if hashtags:
            formatted_caption += "\n\n" + " ".join([f"#{tag}" for tag in hashtags])
        
        # Generate post ID
        post_id = f"post_{int(time.time())}"
        
        # Create post record
        post = {
            "id": post_id,
            "account_id": account_id,
            "media": [
                {
                    "type": self._get_media_type(path),
                    "path": path,
                    "alt_text": f"Image {i+1}" if self._get_media_type(path) == "image" else f"Video {i+1}"
                }
                for i, path in enumerate(valid_media)
            ],
            "caption": formatted_caption,
            "hashtags": hashtags,
            "tagged_users": tagged_users,
            "location": location,
            "created_at": time.time(),
            "scheduled_time": scheduled_time.timestamp() if scheduled_time else None,
            "status": "scheduled" if scheduled_time else "ready",
            "performance": {
                "likes": 0,
                "comments": 0,
                "shares": 0,
                "saves": 0,
                "reach": 0
            }
        }
        
        # If scheduled for immediate posting, publish now
        if not scheduled_time:
            self.publish_post(post_id)
        
        logger.info(f"Post created: {post_id}")
        return post
    
    def _validate_media(self, media_paths: List[str]) -> List[str]:
        """Validate media files for posting.
        
        Args:
            media_paths: Paths to media files
            
        Returns:
            List of valid media paths
        """
        valid_media = []
        
        for path in media_paths:
            # In a real implementation, this would:
            # 1. Check if file exists
            # 2. Validate file type (image/video)
            # 3. Check file size and dimensions
            # 4. Possibly resize/optimize for Instagram
            
            # Simulate validation
            if path and (path.endswith(('.jpg', '.jpeg', '.png', '.mp4'))):
                valid_media.append(path)
            else:
                logger.warning(f"Invalid media file: {path}")
        
        return valid_media
    
    def _get_media_type(self, path: str) -> str:
        """Determine media type from file path.
        
        Args:
            path: Path to media file
            
        Returns:
            Media type ('image' or 'video')
        """
        if path.endswith(('.mp4', '.mov')):
            return "video"
        else:
            return "image"
    
    @Task
    def publish_post(self, post_id: str) -> Dict[str, Any]:
        """Publish a post to Instagram.
        
        Args:
            post_id: ID of the post to publish
            
        Returns:
            Dict containing publish result
        """
        logger.info(f"Publishing post: {post_id}")
        
        # In a real implementation, this would:
        # 1. Retrieve post details from database
        # 2. Get account details
        # 3. Use browser manager to log into the account
        # 4. Navigate to create post interface
        # 5. Upload media, add caption, tags, etc.
        # 6. Submit the post
        
        # Simulate post publishing
        time.sleep(random.uniform(3.0, 6.0))  # Simulate publishing time
        
        publish_result = {
            "post_id": post_id,
            "status": "published",
            "published_at": time.time(),
            "instagram_post_id": f"ig_{random.randint(10000000, 99999999)}"
        }
        
        logger.info(f"Post published: {post_id}")
        return publish_result
    
    @Task
    def track_post_performance(self, post_id: str) -> Dict[str, Any]:
        """Track the performance of a published post.
        
        Args:
            post_id: ID of the post to track
            
        Returns:
            Dict containing performance metrics
        """
        logger.info(f"Tracking performance for post: {post_id}")
        
        # In a real implementation, this would:
        # 1. Retrieve post details from database
        # 2. Use browser manager to log into the account
        # 3. Navigate to the post
        # 4. Scrape performance metrics
        
        # Simulate performance tracking
        time.sleep(random.uniform(1.0, 2.0))  # Simulate tracking time
        
        # Generate random performance metrics for demonstration
        performance = {
            "likes": random.randint(10, 100),
            "comments": random.randint(0, 20),
            "shares": random.randint(0, 10),
            "saves": random.randint(0, 15),
            "reach": random.randint(100, 500),
            "tracked_at": time.time()
        }
        
        logger.info(f"Performance tracked for post: {post_id}")
        return {"post_id": post_id, "performance": performance}
    
    @Task
    def create_batch_posts(self, account_id: str, posts_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple posts in a batch.
        
        Args:
            account_id: ID of the account to post from
            posts_data: List of post data dictionaries
            
        Returns:
            Dict containing batch creation result
        """
        logger.info(f"Creating batch of {len(posts_data)} posts for account: {account_id}")
        
        created_posts = []
        for post_data in posts_data:
            # Create each post
            post = self.create_post(
                account_id=account_id,
                media_paths=post_data.get("media_paths", []),
                caption=post_data.get("caption", ""),
                hashtags=post_data.get("hashtags", []),
                tagged_users=post_data.get("tagged_users", []),
                location=post_data.get("location", ""),
                scheduled_time=post_data.get("scheduled_time")
            )
            created_posts.append(post)
        
        logger.info(f"Batch of {len(created_posts)} posts created for account: {account_id}")
        return {
            "account_id": account_id,
            "posts_created": len(created_posts),
            "post_ids": [post["id"] for post in created_posts],
            "status": "success"
        }