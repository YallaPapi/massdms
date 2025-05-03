# Instagram Automation Tool - User Guide

This guide will help you get started with the Instagram Automation Tool, explaining how to install, configure, and use the tool for common Instagram automation tasks.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Account Management](#account-management)
4. [Messaging Campaigns](#messaging-campaigns)
5. [Content Posting](#content-posting)
6. [Running in Continuous Mode](#running-in-continuous-mode)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.7 or higher
- AdsPower browser (for actual automation)
- Internet connection

### Installation Steps

1. Clone the repository:
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
   ```
   python create_mock_agency_swarm.py
   ```
   This will create a simplified version of agency-swarm that allows the tool to run.

5. Install and set up AdsPower:
   - Download AdsPower from [https://www.adspower.net/](https://www.adspower.net/)
   - Install and start the AdsPower service
   - Ensure the API is enabled (default port: 50325)

6. Configure the tool by editing `config.json` with your settings (see [Configuration](#configuration) section).

## Configuration

The tool uses a JSON configuration file (`config.json`) to store settings. If the file doesn't exist, a default one will be created automatically.

### Example Configuration:

```json
{
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
      "api_key": "your_api_key_here",
      "service": "instagram"
    },
    "email": {
      "provider": "temp_mail"
    }
  },
  "cupidbot": {
    "enabled": true,
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
```

### Configuration Fields:

- **database**: Database settings
  - **type**: Database type (currently only "json" is supported)
  - **path**: Path to the database file

- **adspower**: AdsPower settings
  - **api_url**: AdsPower API URL (default: "http://localhost:50325")
  - **group_id**: AdsPower group ID for profiles

- **verification**: Verification service settings
  - **daisysms**: DaisySMS settings for phone verification
    - **api_key**: Your DaisySMS API key
    - **service**: Service to use (e.g., "instagram")
  - **email**: Email verification settings
    - **provider**: Email provider for verification (e.g., "temp_mail")

- **cupidbot**: CupidBot AI settings
  - **enabled**: Whether CupidBot is enabled
  - **default_personality**: Default personality for the bot
  - **default_response_style**: Default response style for the bot

- **accounts**, **campaigns**, **posts**: Lists of accounts, campaigns, and posts
  - These will be populated as you use the tool

- **logging**: Logging settings
  - **level**: Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
  - **file**: Log file path

## Account Management

### Creating an Account

To create a new Instagram account:

```
python run_improved.py account create --username your_username --password your_password --email your_email@example.com
```

Optional: Add a phone number for verification:
```
python run_improved.py account create --username your_username --password your_password --email your_email@example.com --phone 1234567890
```

### Setting Up a Profile

To set up a profile for an existing account:

```
python run_improved.py account setup-profile --account-id account_id_here --bio "Your bio text" --profile-pic path/to/profile_pic.jpg --external-link https://example.com
```

### Checking Account Health

To check the health status of an account:

```
python run_improved.py account health --account-id account_id_here
```

## Messaging Campaigns

### Creating a Messaging Campaign

To create a messaging campaign targeting followers of a specific account:

```
python run_improved.py message create-campaign --account-ids account_id1,account_id2 --target-source follower_list --target-details '{"account_to_scrape": "target_account"}' --message-templates '[{"content": "Hey there! I love your content!", "sequence_position": 1}, {"content": "Would you be interested in connecting?", "sequence_position": 2}]'
```

To create a campaign targeting users from a text file:

```
python run_improved.py message create-campaign --account-ids account_id1,account_id2 --target-source text_file --target-details '{"file_path": "path/to/usernames.txt"}' --message-templates '[{"content": "Hey there! I love your content!", "sequence_position": 1}]'
```

To enable CupidBot AI conversations, add the `--use-cupidbot` flag:

```
python run_improved.py message create-campaign --account-ids account_id1 --target-source follower_list --target-details '{"account_to_scrape": "target_account"}' --message-templates '[{"content": "Hey there!", "sequence_position": 1}]' --use-cupidbot
```

### Starting a Campaign

To start a campaign immediately:

```
python run_improved.py message start-campaign --campaign-id campaign_id_here
```

To schedule a campaign for later:

```
python run_improved.py message start-campaign --campaign-id campaign_id_here --start-time 2025-05-05T10:00:00
```

### Sending Individual Messages

To send a single message to a specific user:

```
python run_improved.py message send --account-id account_id_here --target-username target_user --message-template '{"content": "Hey there! I love your content!"}'
```

To send with CupidBot AI:

```
python run_improved.py message send --account-id account_id_here --target-username target_user --message-template '{"content": "Hey there!"}' --use-cupidbot
```

## Content Posting

### Creating a Post

To create and schedule a post:

```
python run_improved.py post create --account-id account_id_here --media-paths path/to/image1.jpg,path/to/image2.jpg --caption "Your caption text" --hashtags tag1,tag2,tag3 --scheduled-time 2025-05-05T10:00:00
```

To create a post for immediate publishing:

```
python run_improved.py post create --account-id account_id_here --media-paths path/to/image.jpg --caption "Your caption text" --hashtags tag1,tag2,tag3
```

### Publishing a Post

To manually publish a scheduled post:

```
python run_improved.py post publish --post-id post_id_here
```

### Tracking Post Performance

To track the performance of a post:

```
python run_improved.py post track --post-id post_id_here
```

## Running in Continuous Mode

The tool can run in continuous mode to automatically process scheduled tasks:

```
python run_improved.py run --continuous
```

With custom interval between checks:

```
python run_improved.py run --continuous --interval 300
```

With maximum runtime:

```
python run_improved.py run --continuous --interval 60 --max-runtime 3600
```

## Best Practices

1. **Account Safety**:
   - Use proxies to avoid IP blocks
   - Implement human-like delays between actions
   - Respect Instagram's daily limits for actions
   - Use unique browser profiles for each account
   - Regularly monitor account health

2. **Messaging Campaigns**:
   - Start with small target lists
   - Use personalized messages that look authentic
   - Space out message sending to avoid triggering spam detection
   - Set realistic reply expectations

3. **Content Posting**:
   - Use high-quality images that meet Instagram's standards
   - Write engaging captions with relevant hashtags
   - Schedule posts for optimal times
   - Don't exceed recommended post frequency

4. **Tool Configuration**:
   - Regularly back up your database file
   - Keep AdsPower updated
   - Monitor log files for errors

## Troubleshooting

### Common Issues

#### Agency-Swarm Import Error

If you see an error about missing agency-swarm package:

```
python create_mock_agency_swarm.py
```

#### AdsPower Connection Issues

If the tool can't connect to AdsPower:

1. Ensure AdsPower is running
2. Check the API URL in config.json (default: http://localhost:50325)
3. Verify the AdsPower API is enabled in settings

#### Database Errors

If you encounter database errors:

1. Check if data/database.json exists and is valid JSON
2. Try creating a backup and start with a fresh database

#### Account Creation Failures

If account creation fails:

1. Verify that AdsPower is properly configured
2. Check if the email/phone verification services are working
3. Make sure you're not creating too many accounts in a short period

### Getting Help

If you encounter issues not covered here:

1. Check the log file (default: instagram_automation.log)
2. Review the API documentation in API.md
3. File an issue in the GitHub repository with details of your problem