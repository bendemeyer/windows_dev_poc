import sqlite3

import config


def get_status():
    conn = sqlite3.connect(config.db_filepath)
    cur = conn.cursor()
    sql = """
        SELECT status FROM settings WHERE id=?;
    """
    cur.execute(sql, (config.row_id,))
    row = cur.fetchone()
    conn.close()
    return row[0]


def do_report(status):
    with open(config.report_filepath, 'a+') as file:
        file.write('{status}\n'.format(status=status))


def run():
    status = get_status()
    do_report(status)


if __name__ == '__main__':
    run()