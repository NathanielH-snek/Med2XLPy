import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QGridLayout, QWidget 

class myApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MED2XLPy")
        
        pageLayout = QGridLayout()
        
        menu = self.menuBar()
        #menu.setNativeMenuBar(False)
        fileMenu = menu.addMenu("File")
        def foo():
            print("Gibbity")
        fileMenu.addAction(foo)
        
        
        widget = QWidget()
        
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = myApp()
    sys.exit(app.exec())