# coding=utf-8
import os
from datetime import datetime
from includes.settings import BASE_DIR, NEW_FOLDERS


def append_in_log(text, filename='other'):
    """
    добавление в файл логов

    :param filename: имя файла логов
    :param text: строка лога
    """
    if not os.path.exists(NEW_FOLDERS['logs']):
        os.makedirs(NEW_FOLDERS['logs'])

    with open(BASE_DIR + NEW_FOLDERS['logs'] + filename + '.log', 'a') as logfile:
        logfile.write('%s\t%s\n' % (datetime.now(), text))
