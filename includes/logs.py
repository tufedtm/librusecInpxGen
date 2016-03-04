# coding=utf-8
from time import ctime
from includes.settings import BASE_DIR, NEW_FOLDERS


def append_in_log(filename, text):
    """
    добавление в файл логов

    :param filename: имя файла логов
    :param text: строка лога
    """
    with open(BASE_DIR + NEW_FOLDERS['logs'] + filename + '.log', 'a') as logfile:
        logfile.write('%s\n%s\n\n' % (ctime(), text))
