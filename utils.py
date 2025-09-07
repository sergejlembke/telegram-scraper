import json
# -*- coding: utf-8 -*-
# ======================================
# Telegram Scraper Utility Functions
# ======================================
# This module provides helper functions for scraping, directory management,
# and exporting Telegram chat data to CSV files.
#
# Author: Sergej Lembke
# License: See LICENSE file
# ======================================

# --- Standard library imports ---
import os
from datetime import datetime
from typing import Union, Dict, Any

# --- Third-party imports ---
import pandas as pd

# --- Local module imports ---
from scraping import scraping


def start(start_date: Union[str, datetime, None], end_date: Union[str, datetime, None], chat_id: Union[str, int], project_name: str, api_id: int, api_hash: str, phone_number: str,
          translation_option: Dict[str, Any], export_option: Dict[str, Any], cwd: str) -> None:
    """
    Starts the process of scraping Telegram data for the specified project and parameters.
    This function also handles exporting the scraped data in specified formats.

    Args:
        start_date: The start date for the data to be scraped. Accepts string or datetime
            format, or None if not specified.
        end_date: The end date for the data to be scraped. Accepts string or datetime
            format, or None if not specified.
        chat_id: The chat ID (or username) for the Telegram group or channel.
        project_name: The name of the project that will organize the scraped data.
        api_id: The API ID for authenticating with the Telegram API.
        api_hash: The API hash for authenticating with the Telegram API.
        phone_number: The associated phone number for the Telegram client.
        translation_option: A dictionary specifying translation options for the scraped data.
        export_option: A dictionary specifying export formats (e.g., CSV, JSON) and options
            for the scraped data.
        cwd: The current working directory where outputs will be stored.

    Returns:
        None
    """
    print(f'>>> BEGIN SCRAPING FOR PROJECT: {project_name} <<<')
    cwd_new = os.path.join(str(cwd), 'Scraped_Telegram_Data', str(project_name))
    check_dir(cwd_new)
    data, empty = scraping(start_date, end_date, chat_id, project_name, api_id, api_hash, phone_number, translation_option, cwd_new)
    if 'csv' in export_option['format']:
        export_csv(data, project_name, empty, export_option, cwd_new)
    if 'json' in export_option['format']:
        export_json(data, project_name, empty, export_option, cwd_new)
    print(f'>>> FINISHED SCRAPING FOR PROJECT: {project_name} <<<')
    return

def check_dir(cwd_new):
    """
    Checks and creates a directory if it does not exist.

    This function checks whether a directory specified by the `cwd_new`
    parameter exists. If the directory does not exist, it creates the
    directory.

    Args:
        cwd_new: A path to the directory to check or create. The path
            can be a string or a pathlib.Path object.

    Returns:
        None
    """
    if not os.path.isdir(str(cwd_new)):
        os.makedirs(str(cwd_new))
    return

def export_csv(data, project_name, empty, export_option, cwd_new):
    """
    Exports chat data to a CSV file, with the ability to append to or create new
    CSV files for the specified project. The function also formats the filename
    based on the current date and time.

    Args:
        data: list
            A list of dictionaries containing chat data to be exported. Each
            dictionary represents a row with keys such as 'SENDER_NAME',
            'SENDER_ID', 'MESSAGE_ID', etc.
        project_name: str
            The name of the project, which is used as part of the generated
            filename.
        empty: bool
            A flag indicating whether the data is empty. If True, the function
            will immediately return without performing any operations.
        export_option: dict
            A dictionary containing export options, such as whether to append
            data to an existing file. The dictionary must include a key
            'append' with a boolean value.
        cwd_new: str
            The directory path where the CSV file(s) should be saved.
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

def export_json(data, project_name, empty, export_option, cwd_new):
    """
    Exports data to a JSON file, with an option to append new data to an existing file.
    The function handles extraction, conversion, and saving of chat content into
    a structured JSON format. It generates a timestamp-based filename for the output
    file to ensure uniqueness and facilitates easy searching and tracking of exported files.

    Args:
        data: List of lists containing chat information. Each sublist represents a message
            and contains data elements such as sender name, sender ID, message ID, date,
            message content, translated message, and media path.
        project_name: Name of the project, used for generating the name of the output JSON file.
        empty: Boolean flag to indicate if the data is empty. If True, the function
            immediately returns without performing further processing.
        export_option: Dictionary containing options for export behavior. If the 'append'
            key is set to True, the function appends new data to an existing JSON file if
            one exists.
        cwd_new: Path to the directory where the output JSON file should be saved.

    Returns:
        None

    Raises:
        Will raise an exception if file write operations fail during the JSON export process.

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

    # Build base map by MESSAGE_ID
    new_data = {str(row[2]): row for row in data}  # MESSAGE_ID is at index 2

    if export_option['append']:
        # Find latest JSON file for this project (if any)
        import glob
        pattern = os.path.join(cwd_new, f'{project_name}_data_*.json')
        existing_files = sorted(glob.glob(pattern), reverse=True)

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