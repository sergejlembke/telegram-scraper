# -*- coding: utf-8 -*-
# Last edit: 2024-11-18

import os
from func_aux import start

# Get parent directory of current working directory
pdir = os.path.dirname(os.getcwd())

# Prompt user to enter time frame (in days) in which messages should get searched for
days_back = int(input('Enter time frame (in days, starting from today) to extract messages from: '))

# Enter API id, API hash and phone number of your Telegram API and account
api_id = 123456789
api_hash = 'YourApiHash'
phone_number = '+47123456789'

# To extract data from multiple chats, duplicate the following lines of code from 'def project_123():' until 'project_123()' for each project
# info regarding chat id: For private channels & group chats the format is: -100 and then the channel id 123456..
#                         For public channels the format is: '@abcxyz..' / for chats the format is: 123456..
def project_01():
    project_name = 'Example Private Channel'
    chat_id = -100123456789

    start(days_back, chat_id, project_name, api_id, api_hash, phone_number, pdir)
project_01()


def project_02():
    project_name = 'Example Public Channel'
    chat_id = '@NameOfPublicChannel'

    start(days_back, chat_id, project_name, api_id, api_hash, phone_number, pdir)
project_02()

