# -*- coding: utf-8 -*-
# ===============================
# Telegram Scraper Main Script
# ===============================
# This script extracts messages from specified Telegram chats using the Telegram API.
# Configure your API credentials and specify the chats to scrape below.
#
# Author: Sergej Lembke
# License: See LICENSE file
# ===============================

# --- Standard library imports ---
import os
import json

# --- Local module imports ---
from utils import start

# Use the project root directory (current working directory where main.py runs)
cwd = os.getcwd()

# Prompt the user to enter the time frame for message extraction
start_date = input('Enter start date (YYYY-MM-DD or leave empty for today): ').strip()
end_date = input('Enter end date (YYYY-MM-DD or leave empty for now): ').strip()

# ===============================
# Telegram API Credentials
# ===============================
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api_id = config['api_id']
api_hash = config['api_hash']
phone_number = config['phone_number']

translation_option = config['translation']

export_option = config['export']

chats = config['chats']

for chat in chats:
    chat_name = chat['chat_name']
    chat_id = chat['chat_id']
    # Pass start_date and end_date directly; utils.start will normalize defaults
    start(start_date, end_date, chat_id, chat_name, api_id, api_hash, phone_number, translation_option, export_option, cwd)
