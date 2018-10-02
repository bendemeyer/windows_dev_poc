import sqlite3
import sys
import os
import shutil

import config


def do_setup():
    if not os.path.exists(os.path.join(config.base_path, config.data_directory)):
        os.makedirs(os.path.join(config.base_path, config.data_directory))

    sql = """
        CREATE TABLE IF NOT EXISTS settings (id integer PRIMARY KEY, username text, password text, status text);
    """
    db_conn = sqlite3.connect(config.db_filepath)
    cursor = db_conn.cursor()
    cursor.execute(sql)
    db_conn.commit()
    db_conn.close()


def do_teardown():
    shutil.rmtree(config.base_path)


if __name__ == '__main__':
    arg = sys.argv[1]
    if arg == 'setup':
        do_setup()
    if arg == 'teardown':
        do_teardown()