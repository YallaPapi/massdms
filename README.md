# Instagram Automation Tool

A comprehensive solution for automating Instagram account management, messaging, and content posting. Built using the agency-swarm framework for multi-agent collaboration.

## Features

- **Account Creation and Management**
  - Create Instagram accounts
  - Set up profiles with pictures, videos, bio, and links
  - Verify accounts with phone (DaisySMS) or email

- **Direct Messaging**
  - Target users from follower lists or imported .txt files
  - Send personalized messages
  - AI-powered conversations with CupidBot integration

- **Content Posting**
  - Create and schedule posts with media, captions, and hashtags
  - Batch posting across multiple accounts
  - Track post performance

- **Browser Automation**
  - AdsPower integration for browser profile management
  - Human-like behavior patterns to avoid detection
  - CupidBot plugin activation and management

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/instagram-automation-tool.git
   cd instagram-automation-tool
   ```

2. Check dependencies:
   ```
   python check_dependencies.py
   ```
   This script will check if all required dependencies are installed and provide instructions on how to proceed.

3. Install essential dependencies:
   ```
   pip install -r requirements-minimal.txt
   ```

4. Handle agency-swarm dependency:
   
   The tool uses the agency-swarm framework, which might not be available on PyPI. You have several options:
   
   a. If you have the agency-swarm source code:
      ```
      cd path/to/agency-swarm
      pip install -e .
      cd path/to/instagram-automation-tool
      ```
   
   b. Create and use a mock implementation:
      ```
      python create_mock_agency_swarm.py
      ```
      This will create a simplified version of agency-swarm that allows the tool to run.

5. Install and set up AdsPower:
   - Download AdsPower from [https://www.adspower.net/](https://www.adspower.net/)
   - Install and start the AdsPower service
   - Ensure the API is enabled (default port: 50325)

6. Configure the tool:
   - Edit `config.json` with your settings
   - Add API keys for verification services if needed

## Usage

### Basic Usage

Run the tool with:

```
python instagram_automation_tool.py
```

### Creating Accounts

```python
from instagram_automation_tool import InstagramAutomationTool

tool = InstagramAutomationTool()
account = tool.create_account(
    username="your_username",
    password="your_password",
    email="your_email@example.com",
    phone="1234567890"  # Optional
)
```

### Setting Up Profiles

```python
tool.setup_profile(
    account_id=account["id"],
    bio="Your bio text here",
    profile_pic="path/to/profile_pic.jpg",
    external_link="https://example.com"
)
```

### Creating Messaging Campaigns

```python
campaign = tool.create_messaging_campaign(
    account_ids=[account["id"]],
    target_source="follower_list",
    target_details={
        "account_to_scrape": "target_account"
    },
    message_templates=[
        {
            "content": "Hey there! I love your content!",
            "sequence_position": 1
        }
    ],
    use_cupidbot=True
)
```

### Creating Posts

```python
post = tool.create_post(
    account_id=account["id"],
    media_paths=["path/to/image.jpg"],
    caption="Your caption here",
    hashtags=["instagram", "automation"],
    scheduled_time=None  # Post immediately
)
```

## Security and Best Practices

- Use proxies to avoid IP blocks
- Implement human-like delays between actions
- Respect Instagram's daily limits for actions
- Use unique browser profiles for each account
- Regularly monitor account health

## Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with Instagram's Terms of Service. The developers are not responsible for any misuse or account restrictions that may result from using this tool.

## License

MIT License