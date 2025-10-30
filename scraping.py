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
from datetime import datetime, timezone
from typing import Union, Any

# --- Third-party imports ---
from telethon import TelegramClient
from telethon.tl.types import PeerUser
# NOTE: Import translator lazily inside the function to avoid hard dependency
# from deep_translator import GoogleTranslator

# If running in Spyder or environments with nested event loops, uncomment below:
# import nest_asyncio
# nest_asyncio.apply()


def scraping(start_date: Union[str, datetime, None], end_date: Union[str, datetime, None], chat_id: Union[str, int], chat_name: str, api_id: int, api_hash: str, phone_number: str, translation_option: dict[str, Any], cwd_new: str) -> tuple[list[list[Any]], bool]:
    """
    Extracts and processes messages from a Telegram group or channel for a specified time frame.

    This function connects to a specified Telegram group or channel using provided credentials
    and settings. It extracts messages from the group/channel within a user-specified
    time frame between start_date and end_date. Messages can include text, sender information,
    media (photos or videos), and translation to English if enabled. The extracted data is saved
    along with metadata for further processing or analysis.

    Args:
        start_date: Inclusive start date-time for extraction. If None or empty, defaults to today at 00:00.
        end_date: Inclusive end date-time for extraction. If None or empty, defaults to now.
        chat_id: Unique identifier or username of the chat/group/channel to extract messages from.
        chat_name: Name of the chat used to create a session for storing extracted data.
        api_id: API ID for the Telegram client to connect to the Telegram server.
        api_hash: API hash for the Telegram client to authenticate requests.
        phone_number: Phone number linked to the Telegram account being used.
        translation_option: Configuration for message text translation. Contains options for enabling translation,
            source language, and target language.
        cwd_new: Current working directory or path to save related files such as session, extracted media, etc.

    Returns:
        tuple[list[list[Any]], bool]: A tuple containing a list of message metadata and a boolean `empty`,
            where the list includes details such as sender, message ID, date, text, translation, and file path
            for any downloaded media, and `empty` indicates whether any messages were found.
    """

    # List to collect message data
    data = []

    async def _get_messages():
        # Initialize Telegram client session for this chat
        client = TelegramClient(
            f"{cwd_new}/{chat_name}.session", api_id, api_hash
        )
        await client.connect()

        # Authorize user if not already authorized
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Enter the verification code sent by Telegram: '))

        # Get the entity (chat/channel/group) by chat_id
        chat_entity = await client.get_entity(chat_id)

        # Prepare date range for message extraction
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

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
                        # Make parsed datetime timezone-aware in UTC
                        return datetime.strptime(v, f).replace(tzinfo=timezone.utc)
                    except Exception:
                        pass
                # Fallback: try fromisoformat
                try:
                    dt = datetime.fromisoformat(v)
                    if dt.tzinfo is None:
                        return dt.replace(tzinfo=timezone.utc)
                    return dt.astimezone(timezone.utc)
                except Exception:
                    raise ValueError(f"Unrecognized date format: {val}")
            if isinstance(val, datetime):
                # Ensure tz-aware UTC
                if val.tzinfo is None:
                    return val.replace(tzinfo=timezone.utc)
                return val.astimezone(timezone.utc)
            raise ValueError("start_date/end_date must be datetime, str, or None")

        start_dt = _to_dt(start_date, today_start)
        end_dt = _to_dt(end_date, datetime.now(timezone.utc))

        # Ensure chronological order
        if end_dt < start_dt:
            start_dt, end_dt = end_dt, start_dt

        # Iterate through messages in chronological order starting from start_dt (lower bound)
        async for message in client.iter_messages(chat_entity, offset_date=start_dt, reverse=True):
            # Stop if we moved past the end_dt (messages are increasing in time with reverse=True)
            if message.date > end_dt:
                break
            # Skip anything before the start_dt (shouldn't normally occur due to offset_date)
            if message.date < start_dt:
                continue

            print(f"Extracted Message ID = {message.id} ; Date = {message.date}")

            # Get sender information
            sender = await client.get_entity(PeerUser(message.sender_id))

            # Download media if present in the message
            if message.photo:
                # Save photo as 'photo_<message.id>.jpg'
                media_path = await client.download_media(
                    message.media,
                    file=f"{cwd_new}/{chat_name}_photo_{message.id}.jpg"
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
                    file=f"{cwd_new}/{chat_name}_video_{message.id}.mp4"
                )
            else:
                media_path = ''

            # Translate message text to English using Google Translator (optional, safe)
            translated_text = ''
            if translation_option.get('translate'):
                # If message is empty, set a placeholder to avoid translation errors
                text_to_translate = message.text or ''
                try:
                    from deep_translator import GoogleTranslator  # lazy import
                    translated_text = GoogleTranslator(
                        source=translation_option.get('source_language', 'auto'),
                        target=translation_option.get('target_language', 'en')
                    ).translate(text_to_translate)
                except Exception:
                    # Fallback: skip translation silently if library or network not available
                    translated_text = ''

            # Append extracted information to the data list
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
    asyncio.run(_get_messages())

    # Check if any messages were found in the selected time frame
    if not data:
        print('NO MESSAGES FOUND')
        empty = True
    else:
        empty = False

    return data, empty
