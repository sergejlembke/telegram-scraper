# -*- coding: utf-8 -*-
# ======================================
# Telegram Scraper Utility Functions
# ======================================
# This module provides helper functions for mining, directory management,
# and exporting Telegram chat data to CSV files.
#
# Author: sergejlembke
# License: See LICENSE file
# Last edit: 2024-11-18
# ======================================

# --- Standard library imports ---
import os
from datetime import datetime

# --- Third-party imports ---
import pandas as pd

# --- Local module imports ---
from scraping import scraping

def start(days_back_all, chat_id, project_name, api_id, api_hash, phone_number, cwd):
    """
    Main entry point for mining Telegram messages for a specific project.

    Args:
        days_back_all (int): Number of days to look back for messages.
        chat_id (str|int): Telegram chat/channel/group identifier.
        project_name (str): Name for the current mining project.
        api_id (int): Telegram API ID.
        api_hash (str): Telegram API hash.
        phone_number (str): Telegram account phone number.
        cwd (str): Base directory for storing mined data.
    """
    print(f'>>> BEGIN MINING FOR PROJECT: {project_name} <<<')
    cwd_new = os.path.join(str(cwd), 'Mining_Data', str(project_name))
    checkdir(cwd_new)
    data, empty = scraping(days_back_all, chat_id, project_name, api_id, api_hash, phone_number, cwd_new)
    exportcsv(data, project_name, empty, cwd_new)
    print(f'>>> FINISHED MINING FOR PROJECT: {project_name} <<<')
    return

def checkdir(cwd_new):
    """
    Checks if the target directory exists, and creates it if not.

    Args:
        cwd_new (str): Path to the directory to check/create.
    """
    if not os.path.isdir(str(cwd_new)):
        os.makedirs(str(cwd_new))
    return

def exportcsv(data, project_name, empty, cwd_new):
    """
    Exports harvested Telegram data to a CSV file in the target directory.

    Args:
        data (list): List of extracted message details.
        project_name (str): Name of the mining project.
        empty (bool): True if no messages found, False otherwise.
        cwd_new (str): Directory to save the CSV file.
    """
    if empty:
        return

    date_for_print = datetime.now()

    # Format date and time for filename (YYYY-MM-DD_HH-MM-SS)
    print_year = str(date_for_print.year)
    print_month = f'{date_for_print.month:02d}'
    print_day = f'{date_for_print.day:02d}'
    print_hour = f'{date_for_print.hour:02d}'
    print_minute = f'{date_for_print.minute:02d}'
    print_second = f'{date_for_print.second:02d}'

    date_print = (f'{print_year}-{print_month}-{print_day}_'
                  f'{print_hour}-{print_minute}-{print_second}')

    # Define DataFrame columns for channel/chat exports
    df = pd.DataFrame(data, columns=[
        'CHANNEL TITLE',
        'SENDER ID',
        'MESSAGE ID',
        'DATE',
        'MESSAGE',
        'GOOGLE TRANSLATED MESSAGE',
        # 'DEEPL TRANSLATED MESSAGE',
        'MEDIA'
    ])
    output_path = os.path.join(cwd_new, f'{project_name}_data_{date_print}.csv')
    df.to_csv(output_path, encoding='utf-8', index=False)
    print(f'EXTRACTION COMPLETED. Data saved in: {output_path}')
    return
