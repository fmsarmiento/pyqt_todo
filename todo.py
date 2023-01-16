# To do list that uses sqlite3 as database

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3

# Establish a connection to the database, using SQLITE3
conn = sqlite3.connect('mylist.db')
# Create a cursor. Cursor does the tinkering in the database for you 
c = conn.cursor()
# Create a table if it does not exist
c.execute("""CREATE TABLE if not exists todo_list(
    list_item text
    )""")
# Commit the change
conn.commit()
# Close connection
conn.close()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(438, 346)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.additem_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_it())
        self.additem_pushButton.setGeometry(QtCore.QRect(10, 50, 91, 23))
        self.additem_pushButton.setObjectName("additem_pushButton")
        self.deleteitem_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete_it())
        self.deleteitem_pushButton.setGeometry(QtCore.QRect(104, 50, 111, 23))
        self.deleteitem_pushButton.setObjectName("deleteitem_pushButton")
        self.clearall_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.clear_it())
        self.clearall_pushButton.setGeometry(QtCore.QRect(220, 50, 101, 23))
        self.clearall_pushButton.setObjectName("clearall_pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 411, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 80, 411, 211))
        self.listWidget.setObjectName("listWidget")
        self.savedb_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.save_it())
        self.savedb_pushButton.setGeometry(QtCore.QRect(330, 50, 91, 23))
        self.savedb_pushButton.setObjectName("savedb_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 438, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.grab_all() # Grab items from the database

    # OWN DEFINITIONS HERE
    def add_it(self):
        item = self.lineEdit.text() # Get the text from the input line
        if item != "": # If not empty:
            self.listWidget.addItem(item) # Add the item on the list widget
            self.lineEdit.setText("")

    def delete_it(self):
        clicked = self.listWidget.currentRow() # Get the current highlighted row [index kkukunin mo]
        self.listWidget.takeItem(clicked) # Delete the selected row. We're TAKING IT FROM THE LIST.

    def clear_it(self):
        self.listWidget.clear() # Remove all contents in the listWidget

    def save_it(self): # Save to the database
        conn = sqlite3.connect('mylist.db')
        c = conn.cursor()
        # Delete everything in the database
        c.execute("DELETE FROM todo_list;")
        items = [] # Create list
        for index in range(self.listWidget.count()): # For each item in the list
            items.append(self.listWidget.item(index)) # add list[index] to items
            print(self.listWidget.item(index).text()) # Print the stuff
            c.execute("INSERT INTO todo_list VALUES (:item)",
                {
                    'item': self.listWidget.item(index).text(),
                })
        
        conn.commit()
        conn.close()
        # Pop up box 
        msg = QMessageBox()
        msg.setWindowTitle("Saved to Database!")
        msg.setText("Your To-do list has been saved.")
        msg.setIcon(QMessageBox.Information) # Get information icon
        x = msg.exec_() # Execute the window
    
    def grab_all(self): # Grab items from database
        conn = sqlite3.connect('mylist.db')
        c = conn.cursor()
        c.execute("SELECT * FROM todo_list;")
        records = c.fetchall() # Get all that we got from the execute
        conn.commit()
        conn.close()
        for record in records: # Loop through records, add to screen
            self.listWidget.addItem(str(record[0])) # Records are in tuples. record[0] gets first column, which our record only has 1 column

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "To-Do List"))
        self.additem_pushButton.setText(_translate("MainWindow", "Add"))
        self.deleteitem_pushButton.setText(_translate("MainWindow", "Delete"))
        self.clearall_pushButton.setText(_translate("MainWindow", "Clear"))
        self.savedb_pushButton.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
