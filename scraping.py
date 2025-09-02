
# ======================================
# Telegram Scraper Utility Functions
# ======================================
# This module provides the core scraping logic for extracting messages,
# media, and translations from Telegram chats using the Telethon library.
#
# Author: sergejlembke
# License: See LICENSE file
# ======================================

# --- Standard library imports ---
import asyncio
from datetime import datetime, timedelta

# --- Third-party imports ---
from telethon import TelegramClient
from telethon.tl.types import PeerUser
from deep_translator import GoogleTranslator

# If running in Spyder or environments with nested event loops, uncomment below:
# import nest_asyncio
# nest_asyncio.apply()

def scraping(days_back, chat_id, project_name, api_id, api_hash, phone_number, cwd_new):
    """
    Extracts messages and media from a specified Telegram chat/channel/group.

    Args:
        days_back (int): Number of days to look back for messages.
        chat_id (str|int): Telegram chat/channel/group identifier.
        project_name (str): Name for the current scraping project.
        api_id (int): Telegram API ID.
        api_hash (str): Telegram API hash.
        phone_number (str): Telegram account phone number.
        cwd_new (str): Directory to store session and media files.

    Returns:
        tuple: (data, empty)
            data (list): List of extracted message details.
            empty (bool): True if no messages found, False otherwise.
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

        # Calculate the earliest date for message extraction
        date_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date_today - timedelta(days_back)

        # Iterate through messages, starting from the newest
        async for message in client.iter_messages(group, min_id=0):
            # Stop if message is older than the specified time frame
            if str(message.date) < str(end_date):
                break
            else:
                print(f"Extracted Message ID = {message.id} ; Date = {message.date}")

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
            # If message is empty, set a placeholder to avoid translation errors
            if not message.text:
                message.text = '[THIS MESSAGE CONTAINS NO TEXT]'
            translated_text_google = GoogleTranslator(source='auto', target='en').translate(message.text)
            # For DeepL translation, uncomment and configure your API key:
            # translated_text_deepl = DeeplTranslator(api_key="your_api_key", source="auto", target="en", use_free_api=True).translate(message.text)

            # Append extracted information to the data list
            # For channels, sender.title is used; for chats, sender.username may be more appropriate
            data.append([
                getattr(sender, 'title', getattr(sender, 'username', 'Unknown')),
                message.sender_id,
                message.id,
                message.date,
                message.text,
                translated_text_google,
                # translated_text_deepl,
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
