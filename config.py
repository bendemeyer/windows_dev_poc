import os


base_path = os.path.join(os.environ['APPDATA'], 'WinDevPOC')
if not os.path.exists(base_path):
    os.makedirs(base_path)

data_directory = 'data'
data_path = os.path.join(base_path, data_directory)
if not os.path.exists(data_path):
    os.makedirs(data_path)

db_filename = 'windevpoc.sqlite3'
db_filepath = os.path.join(base_path, data_directory, db_filename)

report_filename = 'report.txt'
report_filepath = os.path.join(base_path, data_directory, report_filename)

row_id = 1
