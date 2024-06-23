import os
import re

from PyQt5.QtGui import QStandardItemModel, QStandardItem      
from PyQt5.QtWidgets import *
from PyQt5 import uic


class MyGui(QMainWindow):

    def __init__(self):

        super(MyGui, self).__init__()
        # we load our ui which we created using the qt designer
        uic.loadUi('bulkgui.ui', self)
        self.show()

        # define default values
        self.directory = "."
        self.listModel = QStandardItemModel()
        self.selectModel = QStandardItemModel()
        

        self.selectView.setModel(self.selectModel)
        # so to have our  functions selected in a list
        self.selected = []

        # our object that have been defined in our QT designer are given individual functions
        self.actionOpen.triggered.connect(self.load_directory)
        self.filterButton.clicked.connect(self.filter_list)
        self.selectButton.clicked.connect(self.choose_selection)
        self.removeButton.clicked.connect(self.remove_selection)
        self.applyButton.clicked.connect(self.rename_files)
        self.actionCrete_New_Folder.triggered.connect(self.create_folder)
        self.changeExtensionButton.clicked.connect(self.change_extension)

    # function to load directory

    def load_directory(self):
        # open of a file Dialog
        self.directory = QFileDialog.getExistingDirectory(
            self, "Select Directory")
        for file in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, file)):
                self.listModel.appendRow(QStandardItem(file))
        self.listView.setModel(self.listModel)

    def rename_files(self):
        counter = 1
        # because we only need to look into the selected list
        try:
            for filename in self.selected:
                if self.addPrefixRadio.isChecked():
                    os.rename(os.path.join(self.directory, filename), os.path.join(
                        self.directory, self.nameEdit.text() + filename))

                elif self.removePreffixRadio.isChecked():
                    if filename.startswith(self.nameEdit.text()):
                        os.rename(os.path.join(self.directory, filename), os.path.join(
                            self.directory, filename[len(self.nameEdit.text()):]))

                elif self.addSuffixRadio.isChecked():
                    filetype = filename.split('.')[-1]
                    os.rename(os.path.join(self.directory, filename), os.path.join(
                        self.directory, filename[:(len(filetype) + 1)] + self.nameEdit.text() + "." + filetype))
                    # os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, filename + self.nameEdit.text() + filetype))

                elif self.removeSuffixRadio.isChecked():
                    filetype = filename.split('.')[-1]
                    if filename.endswith(self.nameEdit.text() + "." + filetype):
                        os.rename(os.path.join(self.directory, filename), os.path.join(
                            self.directory, filename[:-len(self.nameEdit.text() + '.' + filetype)] + "." + filetype))
                elif self.renameRadio.isChecked():
                    filetype = filename.split('.')[-1]
                    os.rename(os.path.join(self.directory, filename), os.path.join(
                        self.directory, self.nameEdit.text() + str(counter) + "." + filetype))
                    counter += 1
                else:
                    print("Select a radio button!")
        except Exception as e:
            print(e)

            self.selected = []
            self.selectModel.clear()
            self.listModel.clear()

            for file in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, file)):
                    self.listModel.appendRow(QStandardItem(file))
            self.listView.setModel(self.listModel)

    def choose_selection(self):
        if len(self.listView.selectedIndexes()) != 0:
            for index in self.listView.selectedIndexes():
                if index.data() not in self.selected:
                    self.selected.append(index.data())
                    self.selectModel.appendRow(QStandardItem(index.data()))

    def remove_selection(self):
        try:
            if len(self.selectView.selectedIndexes()) != 0:
                # index is reversed.sorted because if it's not reversed and the system will try to remove something that's not(has been moved) there which wiil cause an error
                for index in reversed(sorted(self.selectView.selectedIndexes())):
                    self.selected.remove(index.data())
                    self.selectModel.removeRow(index.row())
        except Exception as e:
            print(e)

    def filter_list(self):
        self.selectModel.clear()
        self.selected = []
        for index in range(self.listModel.rowCount()):
            item = self.listModel.item(index)
            # used Regx here
            if re.match(self.filterEdit.text(), item.text()):
                self.selectModel.appendRow(QStandardItem(item.text()))
                self.selected.append(item.text())
    
    
    def create_folder(self):
            # Open a file dialog to select the parent directory
            parent_directory = QFileDialog.getExistingDirectory(self, "Select Parent Directory")
            
            if parent_directory:
                # Open the new folder dialog
                dialog = NewFolderDialog()
                if dialog.exec() == QDialog.Accepted:
                    folder_name = dialog.get_folder_name()
                    if folder_name:
                        # Create the full path for the new folder
                        new_folder_path = os.path.join(parent_directory, folder_name)
                        
                        try:
                            # Create the directory
                            os.makedirs(new_folder_path, exist_ok=True)
                            QMessageBox.information(self, "Success", f"Directory '{new_folder_path}' created successfully!")
                            
                            # List the contents of the new folder
                            self.listModel.clear()
                            for file in os.listdir(new_folder_path):
                                if os.path.isfile(os.path.join(new_folder_path, file)):
                                    self.listModel.appendRow(QStandardItem(file))
                            self.listView.setModel(self.listModel)
                            
                        except Exception as e:
                            QMessageBox.critical(self, "Error", str(e))


    def change_extension(self):
        # Get the new extension from the QLineEdit
        new_extension = self.differentiatorEdit.text().strip()

        if not new_extension.startswith('.'):
            new_extension = '.' + new_extension

        try:
            for filename in self.selected:
                base = os.path.splitext(filename)[0]
                new_filename = base + new_extension
                os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, new_filename))

            # Refresh the list view
            self.selected = []
            self.selectModel.clear()
            self.listModel.clear()

            for file in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, file)):
                    self.listModel.appendRow(QStandardItem(file))
            self.listView.setModel(self.listModel)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))



"""""
    def create_folder(self):
        # Open a file dialog to select the parent directory
        self.directory = QFileDialog.getExistingDirectory(self, "Select Directory")

        if self:
            folder_name = QWidget.nameLineEdit.getText(self, "Enter folder name:")

            if folder_name:
                # Create the full path for the new folder
                new_folder_path = os.path.join(self.directory, folder_name)

                try:
                    # Create the directory
                    os.makedirs(new_folder_path, exist_ok=True)
                    QWidget.QMessageBox.information(self, "Success", f"Directory '{new_folder_path}' created successfully!")
                    
                    # List the contents of the new folder
                    self.listModel.clear()
                    for file in os.listdir(new_folder_path):
                        if os.path.isfile(os.path.join(new_folder_path, file)):
                            self.listModel.appendRow(QStandardItem(file))
                    self.listView.setModel(self.listModel)
                    
                except Exception as e:
                    QWidget.QMessageBox.critical(self, "Error", str(e))
"""


class NewFolderDialog(QDialog):
    def __init__(self):
        super(NewFolderDialog, self).__init__()
        uic.loadUi('newname.ui', self)
        
        # Connect buttons to methods
        self.acceptButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def get_folder_name(self):
        return self.nameLineEdit.text()



def main():
    app = QApplication([])
    window = MyGui()
    window.show()
    app.exec_()


app = QApplication([])
windows = MyGui()
app.exec_()
