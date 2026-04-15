"""
Configuration file for loading environment variables.

Stores sensitive data such as the Telegram bot token.
"""

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Telegram bot token
TG_TOKEN = os.getenv("TG_TOKEN")

# Raise an error if the token is missing
if not TG_TOKEN:
    raise ValueError("TG_TOKEN is not set in the .env file")