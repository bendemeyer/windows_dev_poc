import os

if 'ALLUSERSPROFILE' in os.environ:
    base_path = os.path.join(os.environ['ALLUSERSPROFILE'], 'WinDevPOC')
else:
    base_path = os.path.abspath(os.path.join(os.path.expanduser('~'), '.windevpoc'))

data_directory = 'data'

db_filename = 'windevpoc.sqlite3'
db_filepath = os.path.join(base_path, data_directory, db_filename)

report_filename = 'report.txt'
report_filepath = os.path.join(base_path, data_directory, report_filename)

row_id = 1
