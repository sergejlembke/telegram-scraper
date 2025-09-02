# -*- coding: utf-8 -*-
# Last edit: 2024-11-18


from datetime import datetime
from func_mining import mining
import pandas as pd
import os


def start(days_back_all, chat_id, project_name, api_id, api_hash, phone_number, cwd):
    print('>>> BEGIN MINING FOR PROJECT: ' + str(project_name) + ' <<<')
    cwd_new = str(cwd) + '/Mining_Data/' + str(project_name)
    checkdir(project_name, cwd_new)
    data, empty = mining(days_back_all, chat_id, project_name, api_id, api_hash, phone_number, cwd_new)
    exportcsv(data, project_name, empty, cwd_new)
    print('>>> FINISHED MINING FOR PROJECT: ' + str(project_name) + ' <<<')
    return


def checkdir(project_name, cwd_new):
    # Check if the directory with project_name exists. If not, then create it
    if not os.path.isdir(str(cwd_new)):
        os.makedirs(str(cwd_new))
    return


def exportcsv(data, project_name, empty, cwd_new):
    # E X P O R T    T O    .C S V
    # of the harvested data into a .csv table

    if empty == True:
        return

    date_for_print = datetime.now()

    # Convert single parts of the date into str and add a 0 in front if it's < 10 (to avoid e.g. '3' for month, isteand of '03')
    print_year = str(date_for_print.year)

    if date_for_print.month < 10:
        print_month = '0' + str(date_for_print.month)
    else:
        print_month = str(date_for_print.month)

    if date_for_print.day < 10:
        print_day = '0' + str(date_for_print.day)
    else:
        print_day = str(date_for_print.day)

    if date_for_print.hour < 10:
        print_hour = '0' + str(date_for_print.hour)
    else:
        print_hour = str(date_for_print.hour)

    if date_for_print.minute < 10:
        print_minute = '0' + str(date_for_print.minute)
    else:
        print_minute = str(date_for_print.minute)

    if date_for_print.second < 10:
        print_second = '0' + str(date_for_print.second)
    else:
        print_second = str(date_for_print.second)

    date_print = ( print_year + '-'
                  + print_month + '-'
                  + print_day + '_'
                  + print_hour + '-'
                  + print_minute + '-'
                  + print_second )

    # If it's a Channel, then the first entry should be called 'CHANNEL TITLE' / If it's a chat (group or single), then the first entry should be called 'USERNAME'
    df = pd.DataFrame(data, columns=['CHANNEL TITLE',
                                      'SENDER ID',
                                      'MESSAGE ID',
                                      'DATE',
                                      'MESSAGE',
                                      'GOOGLE TRANSLATED MESSAGE',
                                      #'DEEPL TRANSLATED MESSAGE',
                                      'MEDIA'])
    df.to_csv(cwd_new + '/' + project_name + '_data_' + date_print + '.csv', encoding='utf-8')
    print('EXTRACTION COMPLETED. Data saved in: ' + cwd_new + '/' + project_name + '_data_' + date_print + '.csv')
    return
