# coding=utf-8
import os
from settings import BASE_DIR, NEW_FOLDERS


def get_local_archives(path):
    """
    возвращает список с полными путями к ахривам

    :param path: сканируемая папка
    :return: список
    """
    archives = []

    for item in os.listdir(path):
        if os.path.isfile(path + item):
            archives.append(path + item)

    return archives


def get_online_inp():
    for root, dirs, files in os.walk(BASE_DIR + NEW_FOLDERS['inp']):
        for item in files:
            if item.endswith('online.inp'):
                return os.path.join(root, item)
