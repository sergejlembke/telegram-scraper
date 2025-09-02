# -*- coding: utf-8 -*-
# ===============================
# Telegram Scraper Main Script
# ===============================
# This script extracts messages from specified Telegram chats using the Telegram API.
# Configure your API credentials and specify the chats to scrape below.
#
# Author: sergejlembke
# License: See LICENSE file
# ===============================

# --- Standard library imports ---
import os

# --- Local module imports ---
from utils import start

# Get the parent directory of the current working directory
pdir = os.path.dirname(os.getcwd())

# Prompt the user to enter the time frame (in days) for message extraction
days_back = int(input(
    'Enter the time frame (in days, starting from today) to extract messages from: '
))

# ===============================
# Telegram API Credentials
# ===============================
# Replace the following values with your own Telegram API credentials.
# You can obtain your API ID and API hash from https://my.telegram.org
api_id = 123456789  # Your Telegram API ID
api_hash = 'YourApiHash'  # Your Telegram API hash
phone_number = '+49123456789'  # Your Telegram account phone number

# ===============================
# Chat Identification Information
# ===============================
# To extract data from multiple chats, define a function for each chat as shown below.
#
# Chat ID formats:
#   - Private channels & group chats: '-100' followed by the channel/group ID (e.g., -100123456789)
#   - Public channels: '@channelusername' (e.g., @NameOfPublicChannel)
#   - Regular chats: user ID as a string (e.g., '123456789')
#
# Duplicate and modify the project functions below for each chat you wish to scrape.

def project_01():
    """
    Extract messages from a private channel or group chat.
    Update 'project_name' and 'chat_id' as needed.
    """
    project_name = 'Example Private Channel or Group Chat'
    chat_id = -100123456789

    # Start scraping messages for the specified chat
    start(days_back, chat_id, project_name, api_id, api_hash, phone_number, pdir)

project_01()

def project_02():
    """
    Extract messages from a public channel.
    Update 'project_name' and 'chat_id' as needed.
    """
    project_name = 'Example Public Channel'
    chat_id = '@NameOfPublicChannel'

    # Start scraping messages for the specified chat
    start(days_back, chat_id, project_name, api_id, api_hash, phone_number, pdir)

project_02()

def project_03():
    """
    Extract messages from a regular chat (user-to-user).
    Update 'project_name' and 'chat_id' as needed.
    """
    project_name = 'Example Regular Chat'
    chat_id = '123456789'

    # Start scraping messages for the specified chat
    start(days_back, chat_id, project_name, api_id, api_hash, phone_number, pdir)

project_03()
