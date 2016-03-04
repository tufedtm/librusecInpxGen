# coding=utf-8
import glob
import gzip
import inspect
import json
import os
import shutil
import urllib
import zipfile
from includes.getters import get_local_archives, get_online_inp
from includes.logs import append_in_log
from includes.settings import BASE_DIR, LIBRUSEC_DUMP_FILES, NEW_FOLDERS


def create_folders():
    """
    создает все необходимые папки
    """
    for folder in NEW_FOLDERS:
        if not os.path.exists(folder):
            os.makedirs(folder)


def download_librusec_dump():
    """
    скачивает с оф.сайта последний дамп либрусека
    """
    if not os.path.exists(NEW_FOLDERS['sqlgz']):
        create_folders()

    link = 'http://lib.rus.ec/sql/'

    for item in LIBRUSEC_DUMP_FILES:
        urllib.urlretrieve(link + item, NEW_FOLDERS['sqlgz'] + item)
        append_in_log('%s скачан' % item)


def unpack_librusec_dump():
    """
    распаковывает файлы дампа либрусека
    """
    if not os.path.exists(NEW_FOLDERS['sqlgz']) or not os.listdir(NEW_FOLDERS['sqlgz']):
        download_librusec_dump()

    for item in LIBRUSEC_DUMP_FILES:
        input_file = gzip.open(NEW_FOLDERS['sqlgz'] + item, 'rb')
        output_file = open(NEW_FOLDERS['sql'] + item[:-2], 'wb')
        output_file.write(input_file.read())
        input_file.close()
        output_file.close()
        append_in_log('%s распакован' % item)


def download_lib2inpx(version='64'):
    """
    скачивает последнюю версию lib2inpx

    :param version: указывает какой разрядности версию скачивать
    """
    if not os.path.exists(NEW_FOLDERS['sql']) or not os.listdir(NEW_FOLDERS['sql']):
        unpack_librusec_dump()

    link = 'https://api.github.com/repos/rupor-github/InpxCreator/releases/latest'
    content = json.load(urllib.urlopen(link))

    if version == '32':
        content = content['assets'][0]
    else:
        content = content['assets'][1]

    file_link = content['browser_download_url']
    file_name = content['name']

    urllib.urlretrieve(file_link, NEW_FOLDERS['lib2inpx'] + file_name)
    append_in_log('lib2inpx скачан')


def run_lib2inpx(options='--process all --inpx-format 2.x --db-format 2011-11-06'):
    """
    запускает lib2inpx с заданными параметрами

    :param options: входные параметры для lib2inpx
    """
    lib2inpx = BASE_DIR + NEW_FOLDERS['lib2inpx'] + 'lib2inpx.exe'
    sql_files = BASE_DIR + NEW_FOLDERS['sql']

    os.system('%s %s %s' % (lib2inpx, options, sql_files))

    inpx_src = BASE_DIR + NEW_FOLDERS['lib2inpx'] + 'data/'
    os.chdir(inpx_src)
    inpx_src = inpx_src + glob.glob('*.inpx')[0]
    inpx_dest = BASE_DIR + NEW_FOLDERS['inp']

    shutil.copy(inpx_src, inpx_dest)
    os.chdir(inpx_dest)
    inpxfile = inpx_dest + glob.glob('*.inpx')[0]
    inpxfile = zipfile.ZipFile(inpxfile, 'r')

    if not os.path.exists(inpxfile.filename[:-5]):
        os.makedirs(inpxfile.filename[:-5])

    for item in inpxfile.infolist():
        content = inpxfile.read(item)
        tmp = open(inpxfile.filename[:-5] + '/' + item.filename, 'wb')
        tmp.write(content)
        tmp.close()


def inp_check(inp_file=get_online_inp()):
    """
    создает из входного inp-файла два новых inp-файла
    1. только русские и английские книги
    2. остальные книги

    :param inp_file: путь к файлу online.inp
    """

    inp_input = open(inp_file, 'r')
    inp_output_good = open(BASE_DIR + NEW_FOLDERS['inp'] + 'good.inp', 'w')
    inp_output_bad = open(BASE_DIR + NEW_FOLDERS['inp'] + 'bad.inp', 'w')

    for item in inp_input.readlines():
        tmp = item.split('\x04')

        if tmp[11] in ['ru', 'en']:
            inp_output_good.writelines(item)
        else:
            inp_output_bad.writelines(item)

    inp_input.close()
    inp_output_good.close()
    inp_output_bad.close()


def unpack_good_books(path_to_archives):
    """
    распаковывает из архивов с книгами только файлы соответствующие "хорошим"

    zip_id_mas - массив id книг в архиве
    id_inp - id мусорной книги
    id_bad_inp_mas - массив мусорных id

    :param path_to_archives: путь к папке с архивами
    """
    local_archives = get_local_archives(path_to_archives)

    books_paths = {
        'fb2': 'fb2/',
        'usr': 'usr/',
    }

    for path in books_paths:
        if not os.path.exists(path_to_archives + path):
            os.makedirs(path_to_archives + path)

    for archive in local_archives:
        inp_input = open('inp/online_bad.inp', 'r')
        _zip_input = zipfile.ZipFile(archive, 'r')
        zip_items = _zip_input.namelist()
        zip_id_mas = []

        for item in zip_items:
            zip_id_mas.append(str(str(item).split('.')[:-1])[2:-2])

        id_bad_inp_mas = []
        for item in inp_input.readlines():
            id_bad_inp_mas.append(item.split('\x04')[5])

        for item in zip_id_mas:
            filename = zip_items[zip_id_mas.index(item)]

            if item not in id_bad_inp_mas:
                file_extension = str(filename).split('.')[-1]

                if file_extension == 'fb2':
                    book_path = books_paths['fb2']
                else:
                    book_path = books_paths['usr']

                content = _zip_input.read(filename)

                if not os.path.exists(path_to_archives + book_path + filename):
                    buff = open(path_to_archives + book_path + filename, 'wb')
                    buff.write(content)
                    buff.close()
                    append_in_log(filename + ' извлечен', inspect.stack()[0][3])
                else:
                    append_in_log(filename + ' файл уже был', inspect.stack()[0][3])
            else:
                append_in_log(filename + ' не извлечен, т.к. "плохой"', inspect.stack()[0][3])

        _zip_input.close()
        inp_input.close()

# unpack_good_books('F:\Lib.Rus.Ec + MyHomeLib[FB2+USR]\lib.rus.ec/')
