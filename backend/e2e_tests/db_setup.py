import logging
import subprocess
import warnings
from contextlib import closing

import MySQLdb
from django.conf import settings

E2E_DB = 'jobvyne_cypress'
E2E_DB_SQL_FILE_PATH = './e2e_db.sql'
logger = logging.getLogger(__name__)

# def parse_args():
#     parser = argparse.ArgumentParser(
#         prog='python backend/e2e_tests/db_setup.py',
#         description='Populate the E2E DB or update the SQL build file for the DB'
#     )
#     arg_group = parser.add_mutually_exclusive_group(required=True)
#     arg_group.add_argument(
#         '--rebuild', action='store_true',
#         help='Rebuild the E2E database'
#     )
#     arg_group.add_argument(
#         '--export', action='store_true',
#         help='Update the SQL file used to rebuild the database'
#     )
#     return parser.parse_args()


def _get_sql_connection(**kwargs):
    return MySQLdb.connect(
        db='', host=settings.db_config['HOST'], user=settings.db_config['USER'],
        password=settings.db_config['PASSWORD'], **kwargs
    )


def load_sql_file_to_db(db_name, sql_file_path):
    connection = _get_sql_connection(use_unicode=True, charset='utf8mb4', autocommit=False)
    
    with closing(connection) as connection:
        with connection.cursor() as cursor:
            cursor.execute('set names utf8mb4 collate utf8mb4_bin')

            logger.info(f'Dropping {db_name} database and re-creating it')
            cursor.execute(f'drop database if exists {db_name}')
            cursor.execute(f'create database {db_name} charset utf8mb4 collate utf8mb4_bin')
            connection.commit()
            
            cursor.execute('set FOREIGN_KEY_CHECKS = 0')  # Avoid issue with the order of creating and populating tables with foreign keys
            cursor.execute(f'use {db_name}')
            
            # Get a line count so we can track progress
            with open(sql_file_path, 'r') as sql_file:
                for line_count, _ in enumerate(sql_file, start=1):
                    pass  # This is a noop. We're just using the for loop to enumerate each line

            multi_line_query = ''
            current_line_count = 1
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                logger.info(f'Loading data from {sql_file_path}')
                for line in open(sql_file_path, encoding='utf8'):
                    logger.info(f'Processing line {current_line_count} of {line_count} ({int((current_line_count / line_count) * 100)}% complete)')
                    
                    line = line.rstrip('\n').strip()
                    # Ignore empty lines and comments
                    if not line or line.startswith('/*') or line.startswith('--'):
                        continue
                    
                    multi_line_query += f' {line}'
                    if line.endswith(';'):
                        try:
                            cursor.execute(multi_line_query)
                        except Exception as e:
                            logger.error(f'!!!Query failed on line {current_line_count}: \n{multi_line_query}\n')
                            raise e
                        multi_line_query = ''  # Reset query once the previous one has been executed
                    
                    current_line_count += 1

            cursor.execute('set FOREIGN_KEY_CHECKS = 1')
            connection.commit()
            logger.info(f'Completed populating {db_name} database')


def rebuild_db():
    current_db = settings.db_config['NAME']
    if current_db != E2E_DB:
        logger.error(f'The database must be set to {E2E_DB}. It is currently set to {current_db}')
        exit(-1)
        
    # load_sql_file_to_db()
    

def write_db_to_file(file_path=E2E_DB_SQL_FILE_PATH):
    ''' Note this is currently not functional! The mysqldump command fails because this
    function is run from the backend Docker container while mysql is installed on a separate
    container. I've tried various approaches:
    1) install mysql on the backend container (doesn't work)
    2) call subprocess from the mysql container (not possible to my knowledge)
    :param file_path:
    :return:
    '''
    db_args = [
        '--skip-dump-date', '--skip-comments', '--skip-set-charset', '--skip-lock-tables',
        '--skip-disable-keys', '--skip-add-locks', '--hex-blob', '--triggers',
        '--default-character-set=utf8mb4'
    ]
    db_config = settings.DATABASES['default']
    auth_args = [f'-u {db_config["USER"]}', f'-p {db_config["PASSWORD"]}']
    logger.info(f'Writing to {file_path}')
    with open(file_path, 'wb') as sql_file:
        with subprocess.Popen(
            ['mysqldump', E2E_DB] + auth_args + db_args,
            0, None, subprocess.PIPE, subprocess.PIPE, None
        ) as process:
            for line in process.stdout.readlines():
                sql_file.write(line)
