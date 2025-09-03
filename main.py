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

translate = config['translation']['translate']
source_language = config['translation']['source_language']
target_language = config['translation']['target_language']

export_option = config['export_option']

chats = config['chats']

for chat in chats:
    chat_name = chat['chat_name']
    chat_id = chat['chat_id']
    start(days_back, chat_id, chat_name, api_id, api_hash, phone_number, translate, source_language, target_language, export_option, pdir)
