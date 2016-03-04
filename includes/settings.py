import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'

NEW_FOLDERS = {
    'inp': 'inp/',
    'lib2inpx': 'lib2inpx/',
    'logs': 'logs/',
    'sql': 'sql/',
    'sqlgz': 'sqlgz/',
}

LIBRUSEC_DUMP_FILES = ['libavtor.sql.gz', 'libavtors.sql.gz', 'libbook.sql.gz', 'libgenre.sql.gz',
                       'libgenremeta.sql.gz', 'libgenres.sql.gz', 'libjoinedbooks.sql.gz', 'libmag.sql.gz',
                       'libmags.sql.gz', 'libquality.sql.gz', 'librate.sql.gz', 'libseq.sql.gz', 'libseqs.sql.gz',
                       'libsrclang.sql.gz']
