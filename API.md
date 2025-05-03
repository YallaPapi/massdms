# Instagram Automation Tool - API Documentation

This document provides a comprehensive reference for the Instagram Automation Tool API, including all classes, methods, parameters, and return values.

## Core Classes

### InstagramAutomationTool

The main class for the Instagram Automation Tool.

```python
from instagram_automation_tool_improved import InstagramAutomationTool

# Initialize the tool
tool = InstagramAutomationTool(config_path="config.json")
```

#### Constructor

```python
def __init__(self, config_path: str = "config.json")
```

- **Parameters**:
  - `config_path`: Path to the configuration file (default: "config.json")

#### Methods

##### run

```python
def run(self, continuous: bool = False, interval: int = 60, max_runtime: Optional[int] = None) -> Dict[str, Any]
```

Run the Instagram Automation Tool.

- **Parameters**:
  - `continuous`: Whether to run in continuous mode (periodic checks for scheduled tasks)
  - `interval`: Interval in seconds between checks in continuous mode (default: 60)
  - `max_runtime`: Maximum runtime in seconds for continuous mode (None for indefinite)
- **Returns**:
  - Dict containing run status

##### Account Management Methods

###### create_account

```python
def create_account(self, username: str, password: str, email: str, phone: Optional[str] = None) -> Dict[str, Any]
```

Create a new Instagram account.

- **Parameters**:
  - `username`: Desired username for the account
  - `password`: Password for the account
  - `email`: Email for verification
  - `phone`: Optional phone number for verification
- **Returns**:
  - Dict containing account information

###### setup_profile

```python
def setup_profile(self, account_id: str, bio: str = "", profile_pic: str = "", external_link: str = "") -> Dict[str, Any]
```

Set up an Instagram profile.

- **Parameters**:
  - `account_id`: ID of the account to set up
  - `bio`: Biography text
  - `profile_pic`: Path to profile picture
  - `external_link`: External link for bio
- **Returns**:
  - Dict containing profile setup result

###### check_account_health

```python
def check_account_health(self, account_id: str) -> Dict[str, Any]
```

Check the health status of an account.

- **Parameters**:
  - `account_id`: ID of the account to check
- **Returns**:
  - Dict containing account health information

##### Messaging Methods

###### create_messaging_campaign

```python
def create_messaging_campaign(self, account_ids: List[str], target_source: str, target_details: Dict[str, Any], message_templates: List[Dict[str, Any]], use_cupidbot: bool = False) -> Dict[str, Any]
```

Create a new messaging campaign.

- **Parameters**:
  - `account_ids`: List of account IDs to use for messaging
  - `target_source`: Source of target users ('follower_list' or 'text_file')
  - `target_details`: Details about the target source
  - `message_templates`: List of message templates
  - `use_cupidbot`: Whether to use CupidBot for AI conversations
- **Returns**:
  - Dict containing campaign information

###### start_campaign

```python
def start_campaign(self, campaign_id: str, start_time: Optional[datetime] = None) -> Dict[str, Any]
```

Start a messaging campaign.

- **Parameters**:
  - `campaign_id`: ID of the campaign to start
  - `start_time`: Optional time to start the campaign (None for immediate start)
- **Returns**:
  - Dict containing campaign start result

###### send_message

```python
def send_message(self, account_id: str, target_username: str, message_template: Dict[str, Any], use_cupidbot: bool = False) -> Dict[str, Any]
```

Send a direct message to a target user.

- **Parameters**:
  - `account_id`: ID of the account to send from
  - `target_username`: Username of the target user
  - `message_template`: Template for the message
  - `use_cupidbot`: Whether to use CupidBot for AI conversation
- **Returns**:
  - Dict containing message send result

##### Content Posting Methods

###### create_post

```python
def create_post(self, account_id: str, media_paths: List[str], caption: str, hashtags: List[str] = [], tagged_users: List[str] = [], location: str = "", scheduled_time: Optional[datetime] = None) -> Dict[str, Any]
```

Create and schedule a post.

- **Parameters**:
  - `account_id`: ID of the account to post from
  - `media_paths`: Paths to media files (images/videos)
  - `caption`: Post caption
  - `hashtags`: List of hashtags
  - `tagged_users`: List of users to tag
  - `location`: Location tag
  - `scheduled_time`: When to publish the post
- **Returns**:
  - Dict containing post information

###### publish_post

```python
def publish_post(self, post_id: str) -> Dict[str, Any]
```

Publish a post to Instagram.

- **Parameters**:
  - `post_id`: ID of the post to publish
- **Returns**:
  - Dict containing publish result

###### track_post_performance

```python
def track_post_performance(self, post_id: str) -> Dict[str, Any]
```

Track the performance of a published post.

- **Parameters**:
  - `post_id`: ID of the post to track
- **Returns**:
  - Dict containing performance metrics

###### create_batch_posts

```python
def create_batch_posts(self, account_id: str, posts_data: List[Dict[str, Any]]) -> Dict[str, Any]
```

Create multiple posts in a batch.

- **Parameters**:
  - `account_id`: ID of the account to post from
  - `posts_data`: List of post data dictionaries
- **Returns**:
  - Dict containing batch creation result

## Agent Classes

The tool uses the following agent classes for specialized tasks:

### AccountManagerAgent

Agent responsible for Instagram account creation and management.

#### Methods

##### create_account

```python
def create_account(self, username: str, password: str, email: str, phone: Optional[str] = None) -> Dict[str, Any]
```

Create a new Instagram account.

##### setup_profile

```python
def setup_profile(self, account_id: str, bio: str = "", profile_pic: str = "", external_link: str = "") -> Dict[str, Any]
```

Set up an Instagram profile.

##### check_account_health

```python
def check_account_health(self, account_id: str) -> Dict[str, Any]
```

Check the health status of an account.

### MessagingAgent

Agent responsible for Instagram direct messaging campaigns.

#### Methods

##### create_campaign

```python
def create_campaign(self, account_ids: List[str], target_source: str, target_details: Dict[str, Any], message_templates: List[Dict[str, Any]], use_cupidbot: bool = False) -> Dict[str, Any]
```

Create a new messaging campaign.

##### start_campaign

```python
def start_campaign(self, campaign_id: str, start_time: Optional[datetime] = None) -> Dict[str, Any]
```

Start a messaging campaign.

##### send_message

```python
def send_message(self, account_id: str, target_username: str, message_template: Dict[str, Any], use_cupidbot: bool = False) -> Dict[str, Any]
```

Send a direct message to a target user.

### ContentPosterAgent

Agent responsible for creating and posting Instagram content.

#### Methods

##### create_post

```python
def create_post(self, account_id: str, media_paths: List[str], caption: str, hashtags: List[str] = [], tagged_users: List[str] = [], location: str = "", scheduled_time: Optional[datetime] = None) -> Dict[str, Any]
```

Create and schedule a post.

##### publish_post

```python
def publish_post(self, post_id: str) -> Dict[str, Any]
```

Publish a post to Instagram.

##### track_post_performance

```python
def track_post_performance(self, post_id: str) -> Dict[str, Any]
```

Track the performance of a published post.

##### create_batch_posts

```python
def create_batch_posts(self, account_id: str, posts_data: List[Dict[str, Any]]) -> Dict[str, Any]
```

Create multiple posts in a batch.

### BrowserManagerAgent

Agent responsible for browser automation through AdsPower.

#### Methods

##### create_browser_profile

```python
def create_browser_profile(self, profile_name: str) -> Dict[str, Any]
```

Create a new browser profile in AdsPower.

##### open_browser

```python
def open_browser(self, profile_id: str) -> Dict[str, Any]
```

Open a browser with the specified profile.

##### close_browser

```python
def close_browser(self, profile_id: str) -> Dict[str, Any]
```

Close the browser for the specified profile.

##### navigate

```python
def navigate(self, profile_id: str, url: str) -> Dict[str, Any]
```

Navigate to a URL in the browser.

##### activate_cupidbot

```python
def activate_cupidbot(self, profile_id: str, conversation_id: str) -> Dict[str, Any]
```

Activate CupidBot plugin for a conversation.

##### perform_action

```python
def perform_action(self, profile_id: str, action_type: str, action_params: Dict[str, Any]) -> Dict[str, Any]
```

Perform a browser action.

##### upload_file

```python
def upload_file(self, profile_id: str, file_path: str, upload_selector: str) -> Dict[str, Any]
```

Upload a file in the browser.

## Utility Classes

### Database

Database class for storing and retrieving data.

```python
from utils.database import Database

# Initialize the database
db = Database(config)
```

#### Constructor

```python
def __init__(self, config: Dict[str, Any])
```

- **Parameters**:
  - `config`: Database configuration

#### Methods

##### get_all

```python
def get_all(self, collection: str) -> List[Dict[str, Any]]
```

Get all items from a collection.

- **Parameters**:
  - `collection`: Name of the collection
- **Returns**:
  - List of items in the collection

##### get_by_id

```python
def get_by_id(self, collection: str, item_id: str) -> Optional[Dict[str, Any]]
```

Get an item by ID from a collection.

- **Parameters**:
  - `collection`: Name of the collection
  - `item_id`: ID of the item
- **Returns**:
  - Item if found, None otherwise

##### insert

```python
def insert(self, collection: str, item: Dict[str, Any]) -> Dict[str, Any]
```

Insert an item into a collection.

- **Parameters**:
  - `collection`: Name of the collection
  - `item`: Item to insert
- **Returns**:
  - Inserted item

##### update

```python
def update(self, collection: str, item_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

Update an item in a collection.

- **Parameters**:
  - `collection`: Name of the collection
  - `item_id`: ID of the item to update
  - `updates`: Updates to apply
- **Returns**:
  - Updated item if found, None otherwise

##### delete

```python
def delete(self, collection: str, item_id: str) -> bool
```

Delete an item from a collection.

- **Parameters**:
  - `collection`: Name of the collection
  - `item_id`: ID of the item to delete
- **Returns**:
  - True if item was deleted, False otherwise

##### query

```python
def query(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]
```

Query items in a collection.

- **Parameters**:
  - `collection`: Name of the collection
  - `query`: Query parameters
- **Returns**:
  - List of items matching the query

## Configuration Functions

### load_config

```python
from utils.config_loader import load_config

# Load configuration
config = load_config(config_path)
```

```python
def load_config(config_path: str) -> Dict[str, Any]
```

Load configuration from a JSON file.

- **Parameters**:
  - `config_path`: Path to the configuration file
- **Returns**:
  - Dict containing configuration

### create_default_config

```python
def create_default_config() -> Dict[str, Any]
```

Create a default configuration.

- **Returns**:
  - Dict containing default configuration

### save_config

```python
def save_config(config: Dict[str, Any], config_path: str) -> None
```

Save configuration to a JSON file.

- **Parameters**:
  - `config`: Configuration to save
  - `config_path`: Path to save the configuration to

### validate_config

```python
def validate_config(config: Dict[str, Any]) -> None
```

Validate configuration structure.

- **Parameters**:
  - `config`: Configuration to validate
- **Raises**:
  - `ValueError`: If configuration is invalid