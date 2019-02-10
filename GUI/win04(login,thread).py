# qt 디자이너로 만든 ui를 python에서 로드하여 사용하기
import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import qApp, QMainWindow, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
import os
import requests
import time

'''
signal : 이벤트(클릭..., 사용자 정의 이벤트( emit() )) 발생하는 객체,
 - 정의(1: 디자이너에서 버튼을 끌어서 공간에 던져서 연결 생성
        메인 화면에 pushButton_2, 로그인 화면에 pushButton)
 - 코드에서 직접 생성(2: Work Class 내부에서
                         signal = pyqtSignal()
                        이런식으로 특정 위젯이 아닌 단순 객체로 생성) 
slot : -> signal이 발생하면(이벤트가 발생하면 실제 일을 하는 함수)
    정의
    1. 디자이너에서 툴로 끌어다가 만든 케이스, 코드상에서는 직접 생성만
    2. 코드에서 직접 생성하고 직접 연결한 케이스
'''

login_path = os.getcwd()+'/ui/login.ui'
main_path = os.getcwd()+'/ui/main.ui'
#login_path = 'C:/Users/ChiHoon/Desktop/python_analysis/GUI/ui/login.ui'
print(login_path)

# 제일 나쁜건 수동적으로 따라하기
class LoginForm(QDialog):
    def __init__(self, parent=None):
        #super().__init__(parent) # 왜 super를 쓰지 않는가?
        QDialog.__init__(self, parent)
        self.login_ui = uic.loadUi(login_path, self)
        self.login_ui.show()
        #이렇게 굳이 재정의를 했던 이유? - 클래스라서? 
    # slot 전에는 signal이 있다. 여기서는 click()이다.
    @pyqtSlot()
    def onLogin(self):
        # print('로그인 클릭')
        uid = self.login_ui.input_id.text()
        upw = self.login_ui.input_pw.text()
        res = self.netLogin(uid, upw)
        
        if res['id']==-1:
            # print('로그인 실패')
            QMessageBox.about(self, '알림', '로그인실패')
        else:            
            print('로그인 성공', res['name']+'님 반갑습니다')
            self.close()
            # 메인 윈도우 띄움
            mainwin = MainWin()
            
    def netLogin(self,uid,upw): # 통신만 한다.
        url_str = 'http://164.125.66.70:5000/loginEx'
        res = requests.post(url_str, data={'uid':uid,'upw':upw})
        return res.json()
        #모든 IO는 try catch를 해줘야한다.
     
class MainWin(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.window = uic.loadUi(main_path,self) # 메인창 만들기, 불러오기 self는 왜잇냐
        self.window.show()
        # 쓰레드 생성 및 연결
        self.worker = Worker() # back 에서 구동될 쓰레드
        self.threadObj = QThread() # 쓰레드 객체 생성
        self.worker.moveToThread(self.threadObj) # 가동할 쓰레드 - 쓰레드 객체를 연결
        self.connectionSignal()  # signal 연결 작업
        self.threadObj.start()  # 쓰레드 가동
    

    #쓰레드 중단 버튼을 누르면 호출된다. ?
    def connectionSignal(self):
        # 쓰레드 가동 버튼을 누르면 쓰레드가 시작.
        self.window.pushButton.clicked.connect(self.worker.start)
        # 쓰레드가 돌면서 이벤트를 발생하는데 받을 콜백함수 연결
        self.worker.signal_obj.connect(self.window.recvCnt)# 서로 다른 클래스 끼리 연결
        # 이벤트 이름이 없다.
    #쓰레드가 보내는 숫자값 받는 콜백함수

    #여기는 두개가 있다. signal이 (시작, 종료)
    @pyqtSlot(int)
    def recvCnt(self, cnt):
        self.window.progressBar.setValue(cnt)  # 받아서 화면을 바꿔준다.

    @pyqtSlot()
    def onThreadStop(self):# 이미 연결시켜놓음(디자이너에서)
        if self.threadObj.isRunning():
            self.threadObj.terminate()
            # 플래그 변수 등을 활용하여 반복문도 종료되게 처리
            # 다시 시작하고 싶으면
            # self.threadObj.wait()            
            # self.threadObj.start()    
        

    #쓰레드 걸기
    #쓰레드 도는동안에 

# 쓰레드(프로세스를 잘게 쪼개면 쓰레드가 된다.) 객체
class Worker(QObject):
    # 시그널 담당 객체
    signal_obj = pyqtSignal(int)  # 전에는 디자이너 내에서 해줫음.#int는 1,2,3...
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    @pyqtSlot()
    def start(self):# 자바의 Thread의 run() 메소드
        #0~100까지 계속해서 반복!! 숫자를 생성해서 이벤트를 발생
        cnt = 0
        while cnt < 100: #<- 쓰레드 단위로 쪼개줘야 따로 돈다.
            cnt += 1
            if cnt >= 100:
                cnt = 0
            time.sleep(0.1)

            # 숫자를 증가하면서 시그널(이벤트)을 계속 발생
            self.signal_obj.emit(cnt)  # emit -> 이벤트 발동 함수

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    LoginForm()
    app.exec_()    
    #sys.exit(app.exec_())  # 그냥 x를 누르는것 자체가 종료시키는 것 같다만은 