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
import json

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
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api_id = int(config['api_id'])
api_hash = config['api_hash']
phone_number = config['phone_number']

print(config)
chats = config['chats']

for chat in chats:
    chat_name = chat['chat_name']
    chat_id = chat['chat_id']
    start(days_back, chat_id, chat_name, api_id, api_hash, phone_number, pdir)


# ===============================
# Chat Identification Information
# ===============================
#
# To get the chat ID, login to the web version of Telegram and open the desired chat.
# Click on the chat name at the top to open the chat info, where you can find the chat ID.
#
# Chat ID formats:
#   - Private channels: '-100' followed by the channel ID (e.g., -100123456789)
#   - Public channels: '@channelusername' (e.g., @NameOfPublicChannel)
#   - Group chats: '-100' followed by the group ID (e.g., -100987654321) or '@GroupName'
#   - Regular chats: user ID or username as a string (e.g., '123456789' or '@ExampleUserName')
#
# Duplicate and modify the project functions below for each chat you wish to scrape.
#
# For each chat you want to scrape, you'll get a message with the verification code sent to your Telegram account.
# Enter the code in the terminal when asked for it.
# This is only needed the first time a new chat is added.