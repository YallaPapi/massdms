# Instagram Automation Tool - Installation Guide

This guide provides detailed instructions for installing and setting up the Instagram Automation Tool on different platforms.

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.7 or higher
- **RAM**: Minimum 4GB (8GB+ recommended for multiple accounts)
- **Disk Space**: At least 500MB for the tool + additional space for browser profiles
- **Internet**: Stable connection required
- **Additional Software**: AdsPower browser automation tool

## Installation Steps

### Step 1: Install Python

First, ensure you have Python 3.7+ installed on your system.

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer, ensuring you check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

#### macOS
1. Install Homebrew if not already installed:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python using Homebrew:
   ```
   brew install python
   ```
3. Verify installation:
   ```
   python3 --version
   ```

#### Linux (Ubuntu/Debian)
1. Update package lists:
   ```
   sudo apt update
   ```
2. Install Python:
   ```
   sudo apt install python3 python3-pip python3-venv
   ```
3. Verify installation:
   ```
   python3 --version
   ```

### Step 2: Clone or Download the Repository

#### Using Git
1. Install Git if not already installed
2. Clone the repository:
   ```
   git clone https://github.com/yourusername/instagram-automation-tool.git
   cd instagram-automation-tool
   ```

#### Manual Download
1. Download the ZIP file from the GitHub repository
2. Extract the ZIP file to your desired location
3. Open a terminal/command prompt and navigate to the extracted folder:
   ```
   cd path/to/instagram-automation-tool
   ```

### Step 3: Set Up a Virtual Environment (Recommended)

Creating a virtual environment helps isolate the tool's dependencies from your system Python.

#### Windows
```
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

The tool provides a script to check and install all required dependencies:

```
python check_dependencies.py
```

Alternatively, you can manually install the minimal requirements:

```
pip install -r requirements-minimal.txt
```

### Step 5: Set Up Mock Agency-Swarm

The tool requires the agency-swarm framework, which we'll mock for this installation:

```
python create_mock_agency_swarm.py
```

This script creates a simplified version of agency-swarm that allows the tool to run.

### Step 6: Install and Configure AdsPower

AdsPower is essential for browser automation and profile management:

1. Download AdsPower from [adspower.net](https://www.adspower.net/)
2. Install the application following its installation guide
3. Launch AdsPower and create an account or log in
4. Enable the AdsPower API:
   - Go to Settings > API
   - Enable the API service
   - Note the API port (default is 50325)
   - Make sure the API allows local connections

### Step 7: Configure the Tool

Create or modify the configuration file:

1. If `config.json` doesn't exist, it will be created automatically with defaults
2. Edit the file to match your settings:
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
         "api_key": "",
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

3. Update the `adspower.api_url` if your AdsPower API runs on a different port
4. Add API keys for verification services if you have them

### Step 8: Verify Installation

Run the verification test to ensure everything is set up correctly:

```
python test_import.py
```

This script will check if all dependencies are available and if the tool initializes correctly.

## Platform-Specific Notes

### Windows

- If you encounter permission issues, try running Command Prompt as Administrator
- Ensure Windows Defender or antivirus doesn't block the AdsPower API
- For WebDriver issues, manually install Chrome WebDriver that matches your Chrome version

### macOS

- You may need to allow AdsPower in System Preferences > Security & Privacy
- If using Python from Homebrew, ensure PATH variables are set correctly
- For M1/M2 Macs, ensure you're using the ARM-compatible Python version

### Linux

- You may need additional packages for browser automation:
  ```
  sudo apt install -y xvfb libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libgbm-dev libnss3-dev libxss-dev
  ```
- For headless servers, configure a virtual display with Xvfb:
  ```
  sudo apt install xvfb
  Xvfb :99 -ac &
  export DISPLAY=:99
  ```

## Additional Setup

### Proxy Configuration

For safety and to avoid IP blocks, configure proxies in AdsPower:

1. In AdsPower, go to Group Management
2. Create a new group for Instagram accounts
3. Configure proxy settings for the group
4. Update your `config.json` to use this group ID:
   ```json
   "adspower": {
     "api_url": "http://localhost:50325",
     "group_id": "your_group_id_here"
   }
   ```

### Verification Services

For account creation, you may need phone verification:

1. Sign up for a service like [DaisySMS](https://daisysms.com/)
2. Get your API key
3. Update your `config.json`:
   ```json
   "verification": {
     "daisysms": {
       "api_key": "your_api_key_here",
       "service": "instagram"
     }
   }
   ```

## Troubleshooting

### Common Installation Issues

1. **Python Not Found**: Ensure Python is added to your PATH
2. **Dependency Installation Fails**: Try installing dependencies one by one to identify the problematic package
3. **AdsPower API Not Connecting**: Check if AdsPower is running and the API is enabled with the correct port
4. **Import Errors**: Make sure the mock agency-swarm is installed correctly

### Logs and Debugging

Check the log file for detailed error information:
- Default log location: `instagram_automation.log`
- Set logging level to DEBUG in `config.json` for more detailed logs:
  ```json
  "logging": {
    "level": "DEBUG",
    "file": "instagram_automation.log"
  }
  ```

## Updating

To update the Instagram Automation Tool:

1. Pull the latest changes from the repository:
   ```
   git pull origin main
   ```
   
2. Run the dependency check again:
   ```
   python check_dependencies.py
   ```

3. Check for configuration changes:
   ```
   python run_improved.py config check
   ```

## Next Steps

After completing installation, refer to:
- [USER_GUIDE.md](USER_GUIDE.md) for usage instructions
- [API.md](API.md) for developer reference