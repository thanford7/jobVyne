import logging
import sqlite3
import time

from collections import namedtuple

def company_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple('Company', fields)
    return cls._make(row)

conn = sqlite3.connect('media/companies.sqlite3')
conn.row_factory = company_factory
cursor = conn.cursor()

def get_company_info(company_name, domain):
    for query_col, query_val in (('name', company_name), ('website', domain)):
        start = time.time()
        cursor.execute(f'select * from companies where {query_col} like ?', (query_val,))
        all_rows = cursor.fetchall()
        end = time.time()
        logging.debug(f'Found {len(all_rows)} in {end - start} seconds.')
        if len(all_rows) == 1:
            return all_rows[0]
    return None
