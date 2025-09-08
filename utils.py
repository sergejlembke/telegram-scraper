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
import pathlib
from datetime import datetime
from typing import Union, Dict, Any, Sequence
import json

# --- Third-party imports ---
import pandas as pd

# --- Local module imports ---
from scraping import scraping


def start(start_date: Union[str, datetime, None], end_date: Union[str, datetime, None], chat_id: Union[str, int], chat_name: str, api_id: int, api_hash: str, phone_number: str,
          translation_option: Dict[str, Any], export_option: Dict[str, Any], cwd: str) -> None:
    """
    Starts the scraping process for Telegram data and exports the results based on the specified
    options. The function sets up the working directory, normalizes date formats, and dynamically
    evaluates configured export formats (CSV, JSON) to save the scraped data.

    Args:
        start_date: The start date for the scraping period. Can be a string, datetime, or None.
        end_date: The end date for the scraping period. Can be a string, datetime, or None.
        chat_id: The unique identifier or username of the Telegram chat to scrape data from.
        chat_name: The name of the chat under which the data will be organized and stored.
        api_id: The API ID for the Telegram client used during the scraping process.
        api_hash: The API hash for the Telegram client used during the scraping process.
        phone_number: The phone number linked to the Telegram account for authentication.
        translation_option: Configuration dictionary defining translation options for the scraped data.
        export_option: Configuration dictionary specifying the desired formats and settings for data export.
        cwd: The current working directory where the scraped data will be stored.

    Returns:
        None
    """
    print(f'>>> BEGIN SCRAPING FOR CHAT: {chat_name} <<<')
    cwd_new = os.path.join(str(cwd), 'Scraped_Telegram_Data', str(chat_name))
    check_dir(cwd_new)
    data, empty = scraping(start_date, end_date, chat_id, chat_name, api_id, api_hash, phone_number, translation_option, cwd_new)

    # Build filename suffix based on end_date-start_date
    def _norm_dt(val, default):
        if val is None:
            return default
        if isinstance(val, str):
            v = val.strip()
            if v == "":
                return default
            fmts = [
                "%Y-%m-%d",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d %H:%M:%S",
                "%d.%m.%Y",
                "%d.%m.%Y %H:%M",
                "%d.%m.%Y %H:%M:%S",
            ]
            for f in fmts:
                try:
                    return datetime.strptime(v, f)
                except Exception:
                    pass
            try:
                return datetime.fromisoformat(v)
            except Exception:
                return default
        if isinstance(val, datetime):
            return val
        return default

    start_dt = _norm_dt(start_date, datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    end_dt = _norm_dt(end_date, datetime.now())
    if end_dt < start_dt:
        start_dt, end_dt = end_dt, start_dt

    def _fmt(dt):
        # Always use date only for filename suffix as per requirement
        return dt.strftime('%Y-%m-%d')

    filename_suffix = f"{_fmt(start_dt)}_{_fmt(end_dt)}"

    if 'csv' in export_option['format']:
        export_csv(data, chat_name, empty, export_option, cwd_new, filename_suffix)
    if 'json' in export_option['format']:
        export_json(data, chat_name, empty, export_option, cwd_new, filename_suffix)
    print(f'>>> FINISHED SCRAPING FOR CHAT: {chat_name} <<<')
    return


def check_dir(cwd_new: Union[str, 'pathlib.Path']) -> None:
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


def export_csv(data: Sequence[Sequence[Any]], chat_name: str, empty: bool, export_option: Dict[str, Any], cwd_new: str, filename_suffix: str) -> None:
    """
    Exports data to a CSV file. Handles appending data to an existing CSV file or creating a new one, based on the given 
    export options. If the `empty` flag is True, no action is taken.

    Args:
        data: A list of dictionaries containing export data. Each dictionary represents a single
            row of data with keys matching the default DataFrame column names ('SENDER_NAME', 'SENDER_ID', 'MESSAGE_ID', 
            'DATE', 'MESSAGE', 'TRANSLATED_MESSAGE', 'MEDIA_PATH').
        chat_name: The chat name used for naming the output CSV file.
        empty: A flag to indicate whether the data is empty. If True, the function will return immediately without
            performing any operations.
        export_option: A dictionary containing configuration options for the export process. Supports
            the 'append' key to indicate whether to append to the most recent existing CSV file for the chat.
        cwd_new: The working directory where the CSV file should be saved.
        filename_suffix: The suffix to add as part of the output file name if saving a new file. Ignored when
            appending to an existing file.

    Returns:
        None
    """
    if empty:
        return

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

    # Default: save new data unless appending to an existing dataset
    df_to_save = df_new

    output_path = os.path.join(cwd_new, f'{chat_name}_data_{filename_suffix}.csv')

    if bool(export_option.get('append', False)):
        # Find latest CSV file for this chat (if any)
        import glob
        pattern = os.path.join(cwd_new, f'{chat_name}_data_*.csv')
        existing_files = sorted(glob.glob(pattern), reverse=True)

        if existing_files:
            # Read the most recent CSV file and append to it
            latest_file = existing_files[0]
            df_existing = pd.read_csv(latest_file, encoding='utf-8')
            # Concatenate and drop duplicates by MESSAGE_ID
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined = df_combined.drop_duplicates(subset=['MESSAGE_ID'])
            df_to_save = df_combined
            # Compute oldest and youngest dates across combined data
            try:
                # Ensure DATE is datetime for min/max
                date_series = pd.to_datetime(df_combined['DATE'], errors='coerce')
                min_dt = date_series.min()
                max_dt = date_series.max()
                def _fmt_dt(dt):
                    if pd.isna(dt):
                        return None
                    # Force date-only format in filenames
                    py_dt = dt.to_pydatetime() if hasattr(dt, 'to_pydatetime') else dt
                    return py_dt.strftime('%Y-%m-%d')
                min_str = _fmt_dt(min_dt) or 'unknown'
                max_str = _fmt_dt(max_dt) or 'unknown'
                # Build new target filename reflecting full range
                new_output_path = os.path.join(cwd_new, f'{chat_name}_data_{min_str}_{max_str}.csv')
                # If latest_file already has correct name, overwrite it; otherwise rename
                if os.path.abspath(latest_file) != os.path.abspath(new_output_path):
                    try:
                        os.replace(latest_file, new_output_path)
                        latest_file = new_output_path
                    except Exception:
                        # If rename fails, fall back to writing to new filename
                        latest_file = new_output_path
                output_path = latest_file
            except Exception:
                # Fallback: keep original latest_file name if any error
                output_path = latest_file
            print(f'Appending new chat content and updating file: {output_path}')
        # else: no existing file -> keep df_to_save = df_new and use suffix path

    # Save the updated/new file
    df_to_save.to_csv(output_path, encoding='utf-8', index=False)
    print(f'EXTRACTION COMPLETED. Data saved in: {output_path}')
    return


def export_json(data: Sequence[Sequence[Any]], chat_name: str, empty: bool, export_option: Dict[str, Any], cwd_new: str, filename_suffix: str) -> None:
    """
    Exports the provided chat data to a JSON file. If appending is specified in the 
    export option, it merges the new data with content from the latest JSON file based 
    on the provided chat name. The output JSON file contains structured data for
    each message.

    Args:
        data: Sequence of sequences containing chat data. Each row contains message 
            details such as sender name, sender ID, message ID, timestamp, message 
            content, translated message, and media path.
        chat_name: A string representing the name of the chat to which the
            data belongs.
        empty: A boolean indicating whether the input data is empty. If True, the 
            function terminates early without performing any operations.
        export_option: A dictionary specifying export options. Should include an 
            'append' key to indicate if the new data should be merged with the latest 
            existing JSON file.
        cwd_new: A string representing the directory path where the JSON file should 
            be saved.
        filename_suffix: A string suffix to differentiate the output file if appending 
            is not enabled.

    Raises:
        Exception: If there is an error while reading existing JSON files during the 
            append process.

    Returns:
        None
    """
    if empty:
        return

    # Build base map by MESSAGE_ID
    new_data = {str(row[2]): row for row in data}  # MESSAGE_ID is at index 2

    latest_file = None
    if export_option['append']:
        # Find latest JSON file for this chat (if any)
        import glob
        pattern = os.path.join(cwd_new, f'{chat_name}_data_*.json')
        existing_files = sorted(glob.glob(pattern), reverse=True)

        if existing_files:
            latest_file = existing_files[0]
            with open(latest_file, 'r', encoding='utf-8') as f:
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
            print(f'Appending new chat content and updating file: {latest_file}')

    # Convert dict to list for saving
    final_data = [
        {
            'SENDER_NAME': row[0],
            'SENDER_ID': row[1],
            'MESSAGE_ID': row[2],
            'DATE': str(row[3]),  # Convert datetime to string for the JSON format
            'MESSAGE': row[4],
            'TRANSLATED_MESSAGE': row[5],
            'MEDIA_PATH': row[6]
        }
        for row in new_data.values()
    ]

    # Sort final_data chronologically (oldest to youngest) to match CSV behavior
    try:
        import pandas as _pd
        _dates = _pd.to_datetime([item.get('DATE') for item in final_data], errors='coerce')
        # Build sortable keys: use timestamp seconds for valid dates, else +inf to push NaT to the end
        _keys = []
        for d in _dates:
            try:
                if _pd.isna(d):
                    _keys.append(float('inf'))
                else:
                    _keys.append(d.to_pydatetime().timestamp())
            except Exception:
                _keys.append(float('inf'))
        final_data = [item for _, item in sorted(zip(_keys, final_data), key=lambda t: t[0])]
    except Exception:
        # If parsing fails, leave order as-is
        pass

    # Determine output path: overwrite latest existing when appending, otherwise use suffix
    if export_option.get('append'):
        # Compute min/max date across final_data and rename file accordingly
        try:
            import pandas as _pd
            dates = _pd.to_datetime([item.get('DATE') for item in final_data], errors='coerce')
            min_dt = dates.min()
            max_dt = dates.max()
            def _fmt_dt(dt):
                if _pd.isna(dt):
                    return None
                py_dt = dt.to_pydatetime() if hasattr(dt, 'to_pydatetime') else dt
                return py_dt.strftime('%Y-%m-%d')
            min_str = _fmt_dt(min_dt) or 'unknown'
            max_str = _fmt_dt(max_dt) or 'unknown'
            candidate = os.path.join(cwd_new, f'{chat_name}_data_{min_str}_{max_str}.json')
            # If we had an existing latest file, and its path differs, rename it; otherwise just use candidate path
            if latest_file and os.path.abspath(latest_file) != os.path.abspath(candidate):
                try:
                    os.replace(latest_file, candidate)
                    latest_file = candidate
                except Exception:
                    latest_file = candidate
            output_path = latest_file or candidate
        except Exception:
            output_path = latest_file or os.path.join(cwd_new, f'{chat_name}_data_{filename_suffix}.json')
    else:
        output_path = os.path.join(cwd_new, f'{chat_name}_data_{filename_suffix}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f'EXTRACTION COMPLETED. Data saved in: {output_path}')
    return