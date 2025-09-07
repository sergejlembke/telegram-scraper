# -*- coding: utf-8 -*-
# ======================================
# Telegram Scraper Utility Functions
# ======================================
# This module provides the core scraping logic for extracting messages,
# media, and translations from Telegram chats using the Telethon library.
#
# Author: Sergej Lembke
# License: See LICENSE file
# ======================================

# --- Standard library imports ---
import asyncio
from datetime import datetime, timedelta
from typing import List, Tuple, Union, Dict, Any

# --- Third-party imports ---
from telethon import TelegramClient
from telethon.tl.types import PeerUser
from deep_translator import GoogleTranslator

# If running in Spyder or environments with nested event loops, uncomment below:
# import nest_asyncio
# nest_asyncio.apply()

def scraping(start_date: Union[str, datetime, None], end_date: Union[str, datetime, None], chat_id: Union[str, int], project_name: str, api_id: int, api_hash: str, phone_number: str, translation_option: Dict[str, Any], cwd_new: str) -> Tuple[List[List[Any]], bool]:
    """
    Extracts and processes messages from a Telegram group or channel for a specified time frame.

    This function connects to a specified Telegram group or channel using provided credentials
    and project settings. It extracts messages from the group/channel within a user-specified
    time frame between start_date and end_date. Messages can include text, sender information,
    media (photos or videos), and translation to English if enabled. The extracted data is saved
    along with metadata for further processing or analysis.

    Args:
        start_date (Union[str, datetime, None]): Inclusive start date-time for extraction. If None or empty, defaults to today at 00:00.
        end_date (Union[str, datetime, None]): Inclusive end date-time for extraction. If None or empty, defaults to now.
        chat_id (Union[str, int]): Unique identifier or username of the chat/group/channel to extract messages from.
        project_name (str): Name of the project used to create a session for storing extracted data.
        api_id (int): API ID for the Telegram client to connect to the Telegram server.
        api_hash (str): API hash for the Telegram client to authenticate requests.
        phone_number (str): Phone number linked to the Telegram account being used.
        translation_option (Dict[str, Any]): Configuration for message text translation. Contains options for enabling translation,
            source language, and target language.
        cwd_new (str): Current working directory or path to save related files such as session, extracted media, etc.

    Returns:
        Tuple[List[List[Any]], bool]: A tuple containing a list of message metadata and a boolean `empty`,
            where the list includes details such as sender, message ID, date, text, translation, and file path
            for any downloaded media, and `empty` indicates whether any messages were found.
    """

    # List to collect message data
    data = []

    # Set the start time for message extraction (current time)
    start_time = datetime.now()

    async def get_group_messages():
        # Initialize Telegram client session for this project
        client = TelegramClient(
            f"{cwd_new}/{project_name}.session", api_id, api_hash
        )
        await client.connect()

        # Authorize user if not already authorized
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Enter the verification code sent by Telegram: '))

        # Get the entity (chat/channel/group) by chat_id
        group = await client.get_entity(chat_id)

        # Prepare date range for message extraction
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Normalize input dates
        def _to_dt(val, default):
            if val is None:
                return default
            if isinstance(val, str):
                v = val.strip()
                if v == "":
                    return default
                # Try several common formats
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
                # Fallback: try fromisoformat
                try:
                    return datetime.fromisoformat(v)
                except Exception:
                    raise ValueError(f"Unrecognized date format: {val}")
            if isinstance(val, datetime):
                return val
            raise ValueError("start_date/end_date must be datetime, str, or None")

        start_dt = _to_dt(start_date, today_start)
        end_dt = _to_dt(end_date, datetime.now())

        # Ensure chronological order
        if end_dt < start_dt:
            start_dt, end_dt = end_dt, start_dt

        # Iterate through messages, starting from the newest
        async for message in client.iter_messages(group, min_id=0):
            # Stop if message is older than the specified time frame
            if message.date < start_dt:
                break
            else:
                print(f"Extracted Message ID = {message.id} ; Date = {message.date}")

            # Skip messages newer than end_dt (we iterate from newest to older)
            if message.date > end_dt:
                continue

            # Get sender information
            sender = await client.get_entity(PeerUser(message.sender_id))

            # Download media if present in the message
            if message.photo:
                # Save photo as 'photo_<message.id>.jpg'
                media_path = await client.download_media(
                    message.media,
                    file=f"{cwd_new}/{project_name}_photo_{message.id}.jpg"
                )
            elif (
                hasattr(message, 'media') and
                hasattr(message.media, 'document') and
                hasattr(message.media.document, 'mime_type') and
                message.media.document.mime_type == 'video/mp4'
            ):
                # Save video as 'video_<message.id>.mp4'
                media_path = await client.download_media(
                    message.media,
                    file=f"{cwd_new}/{project_name}_video_{message.id}.mp4"
                )
            else:
                media_path = ''
    
            # Translate message text to English using Google Translator
            if translation_option['translate']:
                # If message is empty, set a placeholder to avoid translation errors
                if not message.text:
                    message.text = '[THIS MESSAGE CONTAINS NO TEXT]'
                translated_text = GoogleTranslator(source=translation_option['source_language'], target=translation_option['target_language']).translate(message.text)
                # For DeepL translation, uncomment and configure your API key:
                # translated_text = DeeplTranslator(api_key="your_api_key", source="auto", target="en", use_free_api=True).translate(message.text)
            else:
                translated_text = ''

            # Append extracted information to the data list
            # For channels, sender.title is used; for chats, sender.username may be more appropriate
            data.append([
                getattr(sender, 'title', getattr(sender, 'username', 'Unknown')),
                message.sender_id,
                message.id,
                message.date,
                message.text,
                translated_text,
                media_path
            ])

    # Run the asynchronous message extraction
    asyncio.run(get_group_messages())

    # Check if any messages were found in the selected time frame
    if not data:
        print('NO MESSAGES FOUND')
        empty = True
    else:
        empty = False

    return data, empty
