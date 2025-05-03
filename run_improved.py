#!/usr/bin/env python3
"""
Run Script for Instagram Automation Tool (Improved)
-------------------------------------------------
This script provides a command-line interface to run the Instagram Automation Tool.
It uses the improved InstagramAutomationTool class with better error handling and
consistent API.
"""

import os
import sys
import argparse
import logging
import json
from datetime import datetime
from instagram_automation_tool_improved import InstagramAutomationTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('instagram_automation.log')
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Instagram Automation Tool')
    
    # Main command
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Account commands
    account_parser = subparsers.add_parser('account', help='Account management commands')
    account_subparsers = account_parser.add_subparsers(dest='account_command', help='Account command to run')
    
    # Create account
    create_account_parser = account_subparsers.add_parser('create', help='Create a new Instagram account')
    create_account_parser.add_argument('--username', required=True, help='Username for the account')
    create_account_parser.add_argument('--password', required=True, help='Password for the account')
    create_account_parser.add_argument('--email', required=True, help='Email for verification')
    create_account_parser.add_argument('--phone', help='Phone number for verification (optional)')
    
    # Setup profile
    setup_profile_parser = account_subparsers.add_parser('setup-profile', help='Set up an Instagram profile')
    setup_profile_parser.add_argument('--account-id', required=True, help='ID of the account')
    setup_profile_parser.add_argument('--bio', help='Biography text')
    setup_profile_parser.add_argument('--profile-pic', help='Path to profile picture')
    setup_profile_parser.add_argument('--external-link', help='External link for bio')
    
    # Check account health
    health_parser = account_subparsers.add_parser('health', help='Check account health')
    health_parser.add_argument('--account-id', required=True, help='ID of the account')
    
    # Messaging commands
    message_parser = subparsers.add_parser('message', help='Messaging commands')
    message_subparsers = message_parser.add_subparsers(dest='message_command', help='Messaging command to run')
    
    # Create campaign
    create_campaign_parser = message_subparsers.add_parser('create-campaign', help='Create a messaging campaign')
    create_campaign_parser.add_argument('--account-ids', required=True, help='Comma-separated list of account IDs')
    create_campaign_parser.add_argument('--target-source', required=True, choices=['follower_list', 'text_file'], help='Source of target users')
    create_campaign_parser.add_argument('--target-details', required=True, help='JSON string with target details')
    create_campaign_parser.add_argument('--message-templates', required=True, help='JSON string with message templates')
    create_campaign_parser.add_argument('--use-cupidbot', action='store_true', help='Use CupidBot for AI conversations')
    
    # Start campaign
    start_campaign_parser = message_subparsers.add_parser('start-campaign', help='Start a messaging campaign')
    start_campaign_parser.add_argument('--campaign-id', required=True, help='ID of the campaign')
    start_campaign_parser.add_argument('--start-time', help='Start time in ISO format (e.g., 2025-04-28T12:00:00)')
    
    # Send message
    send_message_parser = message_subparsers.add_parser('send', help='Send a direct message')
    send_message_parser.add_argument('--account-id', required=True, help='ID of the account to send from')
    send_message_parser.add_argument('--target-username', required=True, help='Username of the target user')
    send_message_parser.add_argument('--message-template', required=True, help='JSON string with message template')
    send_message_parser.add_argument('--use-cupidbot', action='store_true', help='Use CupidBot for AI conversations')
    
    # Post commands
    post_parser = subparsers.add_parser('post', help='Posting commands')
    post_subparsers = post_parser.add_subparsers(dest='post_command', help='Posting command to run')
    
    # Create post
    create_post_parser = post_subparsers.add_parser('create', help='Create a post')
    create_post_parser.add_argument('--account-id', required=True, help='ID of the account')
    create_post_parser.add_argument('--media-paths', required=True, help='Comma-separated list of media paths')
    create_post_parser.add_argument('--caption', required=True, help='Post caption')
    create_post_parser.add_argument('--hashtags', help='Comma-separated list of hashtags')
    create_post_parser.add_argument('--tagged-users', help='Comma-separated list of tagged users')
    create_post_parser.add_argument('--location', help='Location tag')
    create_post_parser.add_argument('--scheduled-time', help='Scheduled time in ISO format (e.g., 2025-04-28T12:00:00)')
    
    # Publish post
    publish_post_parser = post_subparsers.add_parser('publish', help='Publish a post')
    publish_post_parser.add_argument('--post-id', required=True, help='ID of the post to publish')
    
    # Track post performance
    track_post_parser = post_subparsers.add_parser('track', help='Track post performance')
    track_post_parser.add_argument('--post-id', required=True, help='ID of the post to track')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run the tool')
    run_parser.add_argument('--continuous', action='store_true', help='Run in continuous mode')
    run_parser.add_argument('--interval', type=int, default=60, help='Interval in seconds between checks in continuous mode')
    run_parser.add_argument('--max-runtime', type=int, help='Maximum runtime in seconds for continuous mode')
    
    args = parser.parse_args()
    
    # Check if a command was provided
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Check if a subcommand was provided for commands that require one
    if args.command in ['account', 'message', 'post']:
        subcommand_attr = f"{args.command}_command"
        if not getattr(args, subcommand_attr, None):
            # Get the appropriate subparser
            if args.command == 'account':
                subparser = account_parser
            elif args.command == 'message':
                subparser = message_parser
            elif args.command == 'post':
                subparser = post_parser
            
            # Print help for the specific command
            subparser.print_help()
            sys.exit(1)
    
    return args

def main():
    """Run the Instagram Automation Tool."""
    args = parse_arguments()
    
    # Initialize the tool
    tool = InstagramAutomationTool()
    
    # Process commands
    if args.command == 'account':
        process_account_commands(args, tool)
    elif args.command == 'message':
        process_message_commands(args, tool)
    elif args.command == 'post':
        process_post_commands(args, tool)
    elif args.command == 'run':
        run_tool(tool, args)
    else:
        logger.error(f"Unknown command: {args.command}")
        sys.exit(1)

def process_account_commands(args, tool):
    """Process account management commands."""
    if args.account_command == 'create':
        result = tool.create_account(
            username=args.username,
            password=args.password,
            email=args.email,
            phone=args.phone
        )
        
        if result.get("status") == "error":
            logger.error(f"Error creating account: {result.get('message')}")
            sys.exit(1)
        
        logger.info(f"Account created: {result['id']}")
    
    elif args.account_command == 'setup-profile':
        result = tool.setup_profile(
            account_id=args.account_id,
            bio=args.bio or "",
            profile_pic=args.profile_pic or "",
            external_link=args.external_link or ""
        )
        
        if result.get("status") == "error":
            logger.error(f"Error setting up profile: {result.get('message')}")
            sys.exit(1)
        
        logger.info(f"Profile setup completed for account: {args.account_id}")
    
    elif args.account_command == 'health':
        result = tool.check_account_health(
            account_id=args.account_id
        )
        
        if result.get("status") == "error":
            logger.error(f"Error checking account health: {result.get('message')}")
            sys.exit(1)
        
        logger.info(f"Account health status: {result['health']['status']}")
    
    else:
        logger.error(f"Unknown account command: {args.account_command}")
        logger.info("Available account commands: create, setup-profile, health")
        sys.exit(1)

def process_message_commands(args, tool):
    """Process messaging commands."""
    if args.message_command == 'create-campaign':
        try:
            account_ids = args.account_ids.split(',')
            target_details = json.loads(args.target_details)
            message_templates = json.loads(args.message_templates)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            sys.exit(1)
        
        result = tool.create_messaging_campaign(
            account_ids=account_ids,
            target_source=args.target_source,
            target_details=target_details,
            message_templates=message_templates,
            use_cupidbot=args.use_cupidbot
        )
        
        if result.get("status") == "error":
            logger.error(f"Error creating campaign: {result.get('message')}")
            sys.exit(1)
        
        logger.info(f"Campaign created: {result['id']}")
    
    elif args.message_command == 'start-campaign':
        start_time = None
        if args.start_time:
            try:
                start_time = datetime.fromisoformat(args.start_time)
            except ValueError:
                logger.error(f"Invalid datetime format: {args.start_time}. Expected format: YYYY-MM-DDTHH:MM:SS")
                sys.exit(1)
        
        result = tool.start_campaign(
            campaign_id=args.campaign_id,
            start_time=start_time
        )
        
        if result.get("status") == "error":
            logger.error(f"Error starting campaign: {result.get('message')}")
            sys.exit(1)
        
        if start_time:
            logger.info(f"Campaign scheduled to start at {args.start_time}")
        else:
            logger.info(f"Campaign started: {args.campaign_id}")
    
    elif args.message_command == 'send':
        try:
            message_template = json.loads(args.message_template)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            sys.exit(1)
        
        result = tool.send_message(
            account_id=args.account_id,
            target_username=args.target_username,
            message_template=message_template,
            use_cupidbot=args.use_cupidbot
        )
        
        if result.get("status") == "error":
            logger.error(f"Error sending message: {result.get('message')}")
            sys.exit(1)
        
        logger.info(f"Message sent to {args.target_username}")
    
    else:
        logger.error(f"Unknown message command: {args.message_command}")
        logger.info("Available message commands: create-campaign, start-campaign, send")
        sys.exit(1)

def process_post_commands(args, tool):
    """Process posting commands."""
    if args.post_command == 'create':
        try:
            media_paths = args.media_paths.split(',')
            hashtags = args.hashtags.split(',') if args.hashtags else []
            tagged_users = args.tagged_users.split(',') if args.tagged_users else []
        except Exception as e:
            logger.error(f"Error parsing arguments: {str(e)}")
            sys.exit(1)
        
        scheduled_time = None
        if args.scheduled_time:
            try:
                scheduled_time = datetime.fromisoformat(args.scheduled_time)
            except ValueError:
                logger.error(f"Invalid datetime format: {args.scheduled_time}. Expected format: YYYY-MM-DDTHH:MM:SS")
                sys.exit(1)
        
        result = tool.create_post(
            account_id=args.account_id,
            media_paths=media_paths,
            caption=args.caption,
            hashtags=hashtags,
            tagged_users=tagged_users,
            location=args.location or "",
            scheduled_time=scheduled_time
        )
        
        if result.get("status") == "error":
            logger.error(f"Error creating post: {result.get('message')}")
            sys.exit(1)
        
        if scheduled_time:
            logger.info(f"Post scheduled: {result['id']} for {args.scheduled_time}")
        else:
            logger.info(f"Post created: {result['id']}")
    
    elif args.post_command == 'publish':
        result = tool.publish_post(
            post_id=args.post_id
        )
        
        if result.get("status") == "error":
            logger.error(f"Error publishing post: {result.get('message')}")
            sys.exit(1)
        
        logger.info(f"Post published: {args.post_id}")
    
    elif args.post_command == 'track':
        result = tool.track_post_performance(
            post_id=args.post_id
        )
        
        if result.get("status") == "error":
            logger.error(f"Error tracking post performance: {result.get('message')}")
            sys.exit(1)
        
        logger.info(f"Post performance tracked: {args.post_id}")
        logger.info(f"Likes: {result['performance']['likes']}, Comments: {result['performance']['comments']}")
    
    else:
        logger.error(f"Unknown post command: {args.post_command}")
        logger.info("Available post commands: create, publish, track")
        sys.exit(1)

def run_tool(tool, args):
    """Run the tool in continuous or one-shot mode."""
    logger.info("Starting Instagram Automation Tool")
    
    # Extract run parameters
    continuous = getattr(args, 'continuous', False)
    interval = getattr(args, 'interval', 60)
    max_runtime = getattr(args, 'max_runtime', None)
    
    # Run mode info
    if continuous:
        logger.info(f"Running in continuous mode with {interval}s interval")
        if max_runtime:
            logger.info(f"Will stop after {max_runtime}s")
    else:
        logger.info("Running in one-shot mode")
    
    # Run the tool
    result = tool.run(
        continuous=continuous,
        interval=interval,
        max_runtime=max_runtime
    )
    
    # Process result
    if result.get("status") == "error":
        logger.error(f"Error running tool: {result.get('message')}")
        sys.exit(1)
    elif result.get("status") == "stopped":
        logger.info(f"Tool was stopped: {result.get('message')}")
    else:
        logger.info(f"Tool completed successfully: {result.get('message')}")
        if continuous:
            logger.info(f"Completed {result.get('cycles', 0)} cycles")

if __name__ == "__main__":
    main()