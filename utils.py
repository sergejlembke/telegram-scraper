import json
# -*- coding: utf-8 -*-
# ======================================
# Telegram Scraper Utility Functions
# ======================================
# This module provides helper functions for scraping, directory management,
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

def start(days_back_all, chat_id, project_name, api_id, api_hash, phone_number, translation, export_option, cwd):
    """
    Main entry point for scraping Telegram messages for a specific project.

    Args:
        days_back_all (int): Number of days to look back for messages.
        chat_id (str|int): Telegram chat/channel/group identifier.
        project_name (str): Name for the current scraping project.
        api_id (int): Telegram API ID.
        api_hash (str): Telegram API hash.
        phone_number (str): Telegram account phone number.
        cwd (str): Base directory for storing scraped data.
    """
    print(f'>>> BEGIN SCRAPING FOR PROJECT: {project_name} <<<')
    cwd_new = os.path.join(str(cwd), 'Scraped_Telegram_Data', str(project_name))
    checkdir(cwd_new)
    data, empty = scraping(days_back_all, chat_id, project_name, api_id, api_hash, phone_number, translation, cwd_new)
    if 'csv' in export_option['format']:
        exportcsv(data, project_name, empty, export_option , cwd_new)
    if 'json' in export_option['format']:
        exportjson(data, project_name, empty, export_option, cwd_new)
    print(f'>>> FINISHED SCRAPING FOR PROJECT: {project_name} <<<')
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

def exportcsv(data, project_name, empty, export_option, cwd_new):
    """
    Exports harvested Telegram data to a CSV file in the target directory.

    Args:
        data (list): List of extracted message details.
        project_name (str): Name of the scraping project.
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
    df_new = pd.DataFrame(data, columns=[
        'SENDER_NAME',
        'SENDER_ID',
        'MESSAGE_ID',
        'DATE',
        'MESSAGE',
        'TRANSLATED_MESSAGE',
        'MEDIA_PATH'
    ])

    if export_option['append']:
        # Find latest CSV file for this project (if any)
        import glob
        pattern = os.path.join(cwd_new, f'{project_name}_data_*.csv')
        existing_files = sorted(glob.glob(pattern), reverse=True)

        if existing_files:
            # Read the most recent CSV file
            df_existing = pd.read_csv(existing_files[0], encoding='utf-8')
            # Concatenate and drop duplicates by MESSAGE_ID
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined = df_combined.drop_duplicates(subset=['MESSAGE_ID'])
            df_to_save = df_combined
            print(f'Appending new chat content to existing file: {existing_files[0]}')
        else:
            # No existing file, save new data
            df_to_save = df_new

    # Always save the updated file with the current date and time
    output_path = os.path.join(cwd_new, f'{project_name}_data_{date_print}.csv')
    df_to_save.to_csv(output_path, encoding='utf-8', index=False)
    print(f'EXTRACTION COMPLETED. Data saved in: {output_path}')
    return

def exportjson(data, project_name, empty, export_option, cwd_new):
    """
    Exports harvested Telegram data to a JSON file in the target directory.

    Args:
        data (list): List of extracted message details.
        project_name (str): Name of the scraping project.
        empty (bool): True if no messages found, False otherwise.
        cwd_new (str): Directory to save the JSON file.
    """
    if empty:
        return

    date_for_print = datetime.now()
    print_year = str(date_for_print.year)
    print_month = f'{date_for_print.month:02d}'
    print_day = f'{date_for_print.day:02d}'
    print_hour = f'{date_for_print.hour:02d}'
    print_minute = f'{date_for_print.minute:02d}'
    print_second = f'{date_for_print.second:02d}'
    date_print = (f'{print_year}-{print_month}-{print_day}_'
                  f'{print_hour}-{print_minute}-{print_second}')

    if export_option['append']:
        # Find latest JSON file for this project (if any)
        import glob
        pattern = os.path.join(cwd_new, f'{project_name}_data_*.json')
        existing_files = sorted(glob.glob(pattern), reverse=True)

        # Deduplicate by MESSAGE_ID
        new_data = {str(row[2]): row for row in data}  # MESSAGE_ID is at index 2

        if existing_files:
            with open(existing_files[0], 'r', encoding='utf-8') as f:
                try:
                    existing_json = json.load(f)
                except Exception:
                    existing_json = []
            for item in existing_json:
                msg_id = str(item.get('MESSAGE_ID'))
                if msg_id not in new_data:
                    new_data[msg_id] = [
                        item.get('SENDER_NAME'),
                        item.get('SENDER_ID'),
                        item.get('MESSAGE_ID'),
                        item.get('DATE'),
                        item.get('MESSAGE'),
                        item.get('TRANSLATED_MESSAGE'),
                        item.get('MEDIA_PATH')
                    ]
            print(f'Appending new chat content to existing file: {existing_files[0]}')

    # Convert dict to list for saving
    final_data = [
        {
            'SENDER_NAME': row[0],
            'SENDER_ID': row[1],
            'MESSAGE_ID': row[2],
            'DATE': str(row[3]), # Convert datetime to string for the JSON format
            'MESSAGE': row[4],
            'TRANSLATED_MESSAGE': row[5],
            'MEDIA_PATH': row[6]
        }
        for row in new_data.values()
    ]

    output_path = os.path.join(cwd_new, f'{project_name}_data_{date_print}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f'EXTRACTION COMPLETED. Data saved in: {output_path}')
    return