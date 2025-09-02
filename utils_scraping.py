# -*- coding: utf-8 -*-
# Last edit: 2024-11-18

import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.types import PeerUser
from deep_translator import GoogleTranslator
                            #, DeeplTranslator

# If compiled in Spyder, nest_asyncio is needed
#import nest_asyncio
#nest_asyncio.apply()

def mining(days_back, chat_id, project_name, api_id, api_hash, phone_number, cwd_new):


    # File for collection of message data
    data = []

    # Sets the start time to get messages from (start time is set to now)
    start_time = datetime.now()

    async def get_group_messages():
        # Create a Telegram client with the specified API ID, API HASH and PHONE NUMBER
        client = TelegramClient(str(cwd_new) + '/' + str(project_name) + '.session', api_id, api_hash)
        await client.connect()


        # Check if the user is already authorized, otherwise prompt the user to authorize the client
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Enter the verification code send by Telegram: '))

        # Get the ID of the specified group
        group = await client.get_entity(chat_id)

        # Set end date until when the messages should get extracted
        date_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date_today - timedelta(days_back)

        # Go through the messages, starting from newest, until before 'days_back' is reached
        async for message in client.iter_messages(group, min_id=0):
            if str(message.date) < str(end_date):
                break
            else:
                print('Extracted Message ID = ' + str(message.id) + ' ; Date = ' + str(message.date))

            sender = await client.get_entity(PeerUser(message.sender_id))

            # Check if picture is included in message. If so, save picture as 'photo_XYZ' with XYZ=message.id
            if message.photo:
                media_path = await client.download_media(message.media, file = str(cwd_new) + '/' + str(project_name) + 'photo_' + str(message.id) + '.jpg')

            # Check if video is included in message. If so, save video as 'video_XYZ' with XYZ=message.id
            elif (
               hasattr(message, 'media') and
               hasattr(message.media, 'document') and
               hasattr(message.media.document, 'mime_type') and
               message.media.document.mime_type == 'video/mp4'
             ):
                media_path = await client.download_media(message.media, file = str(cwd_new) + '/' + str(project_name) + '_video_' + str(message.id) + '.mp4')
            else:
                media_path = ''


            # T R A N S L A T I O N   W I T H   G O O G L E
            # into preferred language
            # check if message is empty (e.g. a telegram note like 'Channel created' is an empty message, which can't be translated (because it's empty) and therefore the translate tool will give an error and crash the sript)
            if not message.text :
                message.text = '[THIS MESSSAGE CONTAINS NO TEXT]'
            # GoogleTranslate
            translated_text_google = GoogleTranslator(source='auto', target='en').translate(message.text)
            # Deepl
            #translated_test_deepl = DeeplTranslator(api_key="your_api_key", source="auto", target="en", use_free_api=True).translate(message.text)

            # Add specific information from current message into new row in 'data'
            # If it's a Channel, then the first entry should be sender.title / If it's a chat (group or single), then the first entry should be sender.username
            data.append([sender.title,
                         message.sender_id,
                         message.id,
                         message.date,
                         message.text,
                         translated_text_google,
                         #translated_text_deepl,
                         media_path])

    asyncio.run(get_group_messages())

    # Check if there are messages found in the selected time frame
    if not data:
        print('NO MESSAGES FOUND')
        empty = True
    else:
        empty = False

    return data, empty
