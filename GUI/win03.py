# qt 디자이너로 만든 ui를 python에서 로드하여 사용하기
import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import qApp
import os

class WinForm():
    window = None
    def __init__(self,window):
        self.window = window
        print(type(self.window))
        #self.window.show()
        self.window.actionQuit.setShortCut('Ctrl+Q')
        #signal / slot
        self.window.actionQuit.triggered.connect(qApp.quit())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    window = uic.loadUi('C:/Users/ChiHoon/Desktop/python_analysis/GUI/ui/test.ui')
    #window = uic.loadUi(os.getcwd()+'/ui/test.ui')  # 왜 상대경로 인식을 못하니?
    
    WinForm(window)
    window.show()
    sys.exit(app.exec_())