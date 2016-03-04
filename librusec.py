# coding=utf-8
import gzip
import json
import os
import urllib
import zipfile

new_folders = {
    'sqlgz': 'sqlgz/',
    'sql': 'sql/',
    'lib2inpx': 'lib2inpx/'
}

files = ['libavtor.sql.gz', 'libavtors.sql.gz', 'libbook.sql.gz', 'libgenre.sql.gz', 'libgenremeta.sql.gz',
         'libgenres.sql.gz', 'libjoinedbooks.sql.gz', 'libmag.sql.gz', 'libmags.sql.gz', 'libquality.sql.gz',
         'librate.sql.gz', 'libseq.sql.gz', 'libseqs.sql.gz', 'libsrclang.sql.gz']


def create_folders():
    """
    создает все необходимые папки
    """
    for folder in new_folders:
        if os.path.exists(folder):
            print(folder + ' has already been created')
        else:
            os.makedirs(folder)
            print(folder + ' is created')


def download_librusec_dump():
    """
    скачивает с оф.сайта последний дамп либрусека
    """
    create_folders()
    link = 'http://lib.rus.ec/sql/'

    for item in files:
        urllib.urlretrieve(link + item, new_folders['sqlgz'] + item)
        print(item + ' is downloaded')


def unpack_librusec_dump():
    """
    распаковывает файлы дампа либрусека
    """
    download_librusec_dump()
    for item in files:
        input_file = gzip.open(new_folders['sqlgz'] + item, 'rb')
        output_file = open(new_folders['sql'] + item[:-2], 'wb')
        output_file.write(input_file.read())
        input_file.close()
        output_file.close()


def download_lib2inpx(version='64'):
    """
    скачивает последнюю версию lib2inpx

    :param version: указывает какой разрядности версию скачивать
    """
    link = 'https://api.github.com/repos/rupor-github/InpxCreator/releases/latest'
    content = json.load(urllib.urlopen(link))

    if version == '32':
        content = content['assets'][0]
    else:
        content = content['assets'][1]

    file_link = content['browser_download_url']
    file_name = content['name']

    urllib.urlretrieve(file_link, new_folders['lib2inpx'] + file_name)


def inp_check(inp_file):
    """
    создает из входного inp-файла два новых inp-файла
    1. только русские и английские книги
    2. остальные книги

    :param inp_file: исходный inp-файл
    """
    inp_input = open(inp_file, 'r')
    inp_output_good = open('inp/online_good.inp', 'w')
    inp_output_bad = open('inp/online_bad.inp', 'w')

    for item in inp_input.readlines():
        tmp = item.split('\x04')

        if tmp[11] in ['ru', 'en']:
            inp_output_good.writelines(item)
        else:
            inp_output_bad.writelines(item)

    inp_input.close()
    inp_output_good.close()
    inp_output_bad.close()


def archive_del_bad(zip_input):
    """
    удаляет из архива:
    файлы на не русском и английском

    zip_id_mas - массив id книг в архиве
    id_inp - id мусорной книги
    id_bad_inp_mas - массив мусорных id

    :param zip_input: архив с книгами с расширением zip
    """
    # todo: path for fb2 and usr
    books_path = os.path.dirname(zip_input) + '/books/'
    inp_input = open('inp/online_bad.inp', 'r')
    _zip_input = zipfile.ZipFile(zip_input, 'r')
    # zip_output = zipfile.ZipFile(zip_input[:-4] + '_new.zip', 'w', allowZip64=True)
    zip_items = _zip_input.namelist()
    zip_id_mas = []

    if not os.path.exists(books_path):
        os.makedirs(books_path)

    for item in zip_items:
        zip_id_mas.append(str(str(item).split('.')[:-1])[2:-2])

    id_bad_inp_mas = []
    for item in inp_input.readlines():
        id_bad_inp_mas.append(item.split('\x04')[5])

    for item in zip_id_mas:

        if item not in id_bad_inp_mas:
            name = zip_items[zip_id_mas.index(item)]
            content = _zip_input.read(name)
            buff = open(books_path + name, 'wb')
            buff.write(content)
            buff.close()

    # zip_output.close()
    _zip_input.close()
    inp_input.close()

# path = 'F:/Lib.Rus.Ec + MyHomeLib[FB2+USR]/lib.rus.ec/local/'
# archives = []
# for (dirpath, dirnames, filenames) in os.walk(path):
#     archives.extend(filenames)
#
# for archive in archives:
#     archive_del_bad(path + archive)
