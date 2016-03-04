# coding=utf-8
import os


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
