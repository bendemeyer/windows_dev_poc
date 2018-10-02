import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,
    QGridLayout, QLabel, QLineEdit, QSpacerItem, QMessageBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets

import config
 
class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'PatientPop Settings'
        self.db_conn = sqlite3.connect(config.db_filepath)
        self.set_up_settings_table()
        self.initUI()

    def set_up_settings_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS settings (id integer PRIMARY KEY, username text, password text, status text);
        """
        cursor = self.db_conn.cursor()
        cursor.execute(sql)

    def get_settings(self):
        sql = """
            SELECT username, password, status FROM settings WHERE id=?;
        """
        cursor = self.db_conn.cursor()
        cursor.execute(sql, (config.row_id,))
        result = cursor.fetchone()
        if not result:
            result = ('', '', '')
        return result

    def write_fields_to_db(self):
        insert_sql = """
            INSERT OR IGNORE INTO settings (id) VALUES (?);
        """
        cursor = self.db_conn.cursor()
        cursor.execute(insert_sql, (config.row_id,))

        update_sql = """
            UPDATE settings SET username=?, password=?, status=? WHERE id=?;
        """
        cursor.execute(update_sql, (self.username_textbox.text(), self.password_textbox.text(), self.status_textbox.text(), config.row_id))
 
    def initUI(self):
        self.setWindowTitle(self.title)
 
        self.create_grid_layout()
        self.create_horizontal_layout()

        username, password, status = self.get_settings()

        self.username_textbox.setText(username)
        self.password_textbox.setText(password)
        self.confirm_password_textbox.setText(password)
        self.status_textbox.setText(status)
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.gridGroupBox)
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def create_grid_layout(self):
        self.gridGroupBox = QGroupBox()
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)

        self.username_textbox = QLineEdit(self)
        self.password_textbox = QLineEdit(self)
        self.password_textbox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_textbox = QLineEdit(self)
        self.confirm_password_textbox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.status_textbox = QLineEdit(self)
 
        layout.addWidget(QLabel('Username'), 0, 0) 
        layout.addWidget(self.username_textbox, 0, 1)
        layout.addWidget(QLabel('Password'), 1, 0) 
        layout.addWidget(self.password_textbox, 1, 1)
        layout.addWidget(QLabel('Confirm\nPassword'), 2, 0) 
        layout.addWidget(self.confirm_password_textbox, 2, 1)
        layout.addWidget(QLabel('Status'), 3, 0)
        layout.addWidget(self.status_textbox, 3, 1)

        layout.setVerticalSpacing(20)
        layout.setColumnMinimumWidth(0, 100)
        layout.setColumnMinimumWidth(1, 300)
 
        self.gridGroupBox.setLayout(layout)

    def create_horizontal_layout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel_changes)
        layout.addWidget(self.cancel_button)

        layout.addItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding))
        layout.setDirection(QHBoxLayout.RightToLeft)
        
        self.horizontalGroupBox.setLayout(layout)

    def remove_all_validation_formatting(self):
        fields = [self.username_textbox, self.password_textbox, self.confirm_password_textbox]
        for field in fields:
            field.setStyleSheet('')

    def validate_required_fields(self):
        required_fields = [self.username_textbox, self.password_textbox, self.confirm_password_textbox]
        empty_fields = []
        for field in required_fields:
            if field.text() == '':
                empty_fields.append(field)
        if empty_fields:
            for field in empty_fields:
                self.textbox_validation_formatter(field)
            QMessageBox.warning(self, 'Validation Error', 'Please enter a value for all required fields!', QMessageBox.Ok, QMessageBox.Ok)
            return False
        return True

    def validate_password_fields(self):
        password_fields = (self.password_textbox, self.confirm_password_textbox)
        if password_fields[0].text() != password_fields[1].text():
            for field in password_fields:
                self.textbox_validation_formatter(field)
            QMessageBox.warning(self, 'Validation Error', 'Passoword fields must match!', QMessageBox.Ok, QMessageBox.Ok)
            return False
        return True

    @pyqtSlot()
    def save_changes(self):
        self.remove_all_validation_formatting()
        valid = self.validate_required_fields()
        if not valid:
            return
        valid = self.validate_password_fields()
        if not valid:
            return
        self.write_fields_to_db()
        self.db_conn.commit()
        self.db_conn.close()
        self.close()

    @pyqtSlot()
    def cancel_changes(self):
        self.close()

    @staticmethod
    def textbox_validation_formatter(textbox):
        textbox.setStyleSheet('border: 3px solid #bb0000;')


 
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())