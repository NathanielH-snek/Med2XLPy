import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QGridLayout, QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

from pathlib import Path

from utils import readFile, parseFile, saveData

class myApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.outputType = 'Excel'
        self.userHome = Path.home()
        #self.filePath = f"{self.userHome}/MedPC"
        self.filePath = '/Users/11nho/Developer/MedPC/GUITEST'
        self.setWindowTitle('MED2XLPy')
        self.setWindowIcon(QIcon('icon.jpg'))
        
        menu = self.menuBar()
        
        fileMenu = menu.addMenu('File')
        fileSubmenu = fileMenu.addMenu('Output')
        
        self.excelOpt = QAction(self, text='Excel')
        self.excelOpt.setStatusTip('Select File Output Type')
        self.excelOpt.triggered.connect(self.setOutputType)
        self.excelOpt.setCheckable(True)
        self.excelOpt.setChecked(True)
        
        fileSubmenu.addAction(self.excelOpt)
        
        
        self.pageLayout = QGridLayout()
        self.actionMenuLayout = QHBoxLayout()
        
        self.outPath = QLabel(self.filePath)
        self.actionMenuLayout.addWidget(self.outPath)
        
        self.dirButton = QPushButton('Set Directory')
        self.dirButton.clicked.connect(self.setOutputDirectory)
        self.actionMenuLayout.addWidget(self.dirButton)
        
        self.actionButton = QPushButton('Convert')
        self.actionButton.clicked.connect(self.convertData)
        self.actionMenuLayout.addWidget(self.actionButton)
        
        self.pageLayout.addLayout(self.actionMenuLayout, 0,0, Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(self.pageLayout)
        self.setCentralWidget(widget)
        self.show()

    def setOutputType(self,s):
        sender = self.sender()
        if s == True:
            self.outputType = sender.text()
            print(self.outputType)
        else:
            self.outputType = 'Excel'
            self.excelOpt.setChecked(True)
    
    def setOutputDirectory(self):
        directory = QFileDialog.getExistingDirectory(
            caption='Select folder to output files'
            )
        if directory:
            self.filePath = f"{Path(directory)}"
            self.outPath.setText(self.filePath)
        
    def convertData(self):
        files,filetyping = QFileDialog.getOpenFileNames(
            dir=str(self.userHome),
            caption='Select files to convert',
            filter="Text Files (*.txt *.csv *.jpg)"
            )
        if files:
            for file in files:
                contents = readFile(file)
                saveData(parseFile(contents),folderpath=self.outPath.text())
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = myApp()
    sys.exit(app.exec())