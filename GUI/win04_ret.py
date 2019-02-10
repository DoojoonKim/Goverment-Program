from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import qApp, QMainWindow, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
import os
import sys
import time

main_path = os.getcwd()+'/ui/main.ui'

class Login():
    pass


# 상속 받는게 의미상으로는 이해가 간다.
# 근데 이 코드중 어디에서 쓴ㄱ너지 잘 이해가 안간다.
# 생각해보니 self 자체가 클래스이고
# uic_loadUi에 self의 self는 QtWidgets 또는 그의 자식을 상속 받아야 하나 보다.
class MainWin(QMainWindow):# 부모 객체를 왜 상속 받은건지..
    def __init__(self,parent=None):
        # ui 불러오기
        QMainWindow.__init__(self,parent)
        self.window = uic.loadUi(main_path,self) # self 들어가는게 무슨 의미?
        self.window.show()
        self.worker = Worker()
        self.connectionSignal()
    # 버튼 
    # signal 
    # if PushButton.click(): start(worker를)
    #=>
    def connectionSignal(self):#?? 이게 if 문이어야한다고 생각하는데..
        # 사실 signal과 slot을 연결하는 부분이라 생각함. =>O

        # click하면 시작 되도록함.
        self.window.pushButton.clicked.connect(self.worker.start)
        # 이렇게 분해가 된 이유는 worker라는 쓰레드랑 연결해주기 위함임.
        # 근데 시작하고 나서 그 결과 값을 받아 줄 것이 필요
        self.worker.signal_obj.connect(self.window.recvCnt)
        #recvCnt는 바에다가 갱신해주는 의미의 함수일듯
        #start로 계속해서 emit 되는 cnt를 그대로 window.recvCnt로 전달 해준다고 생각함.

    # 바가 있다.
    # 버튼을 누르면 바의 숫자가 계속 해서 올라가는 동작을 취하고 싶다.
    
    @pyqtSlot(int)# ?? int 이거 의미 잘 모르겟
    def recvCnt(self, cnt): # signal이 없음.=> worker가 signal 생성 

        self.window.progressBar.setValue(cnt) 
        # ?? cnt를 연결하는 과정?
        # cnt를 어디서 받아 오는가?
        # worker.start님 께서 return을 해주시는걸까
        
        
        
    @pyqtSlot()
    def onThreadStop(self):
        pass


#bar의 게이지가 1~100까지 증가한다.
class Worker(QObject):#왜 QObject인지는 잘모르겟
    # 시그널 담당 객체
    signal_obj = pyqtSignal(int) # ?? 이거 이때까지 한거 다시 연결 해줘야함.
    def __init__(self,parent=None):
        super(self.__class__, self).__init__(parent)
        # ?? worker는 super고 mainwin은 클래스 이름으로 생성해준 이유가

        print(self.__class__)
    #@pyqtSlot()이 붙어 잇는건 노이해
    # =>start 동작 자체가 무명의 signal을 받음으로써 출력이 됨
    @pyqtSlot() 
    def start(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            time.sleep(0.1)
            self.signal_obj.emit(cnt)
        
    


        




# class MainWin(QMainWindow):
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self,parent)
#         self.window = uic.loadUi(main_path,self) # 메인창 만들기, 불러오기 self는 왜잇냐
#         self.window.show()
#         # 쓰레드 생성 및 연결
#         self.worker = Worker() # back 에서 구동될 쓰레드
#         self.threadObj = QThread() # 쓰레드 객체 생성
#         self.worker.moveToThread(self.threadObj) # 가동할 쓰레드 - 쓰레드 객체를 연결
#         self.connectionSignal()  # signal 연결 작업
#         self.threadObj.start()  # 쓰레드 가동
    

#     #쓰레드 중단 버튼을 누르면 호출된다. ?
#     def connectionSignal(self):
#         # 쓰레드 가동 버튼을 누르면 쓰레드가 시작.
#         self.window.pushButton.clicked.connect(self.worker.start)
#         # 쓰레드가 돌면서 이벤트를 발생하는데 받을 콜백함수 연결
#         self.worker.signal_obj.connect(self.window.recvCnt)# 서로 다른 클래스 끼리 연결
#         # 이벤트 이름이 없다.
#     #쓰레드가 보내는 숫자값 받는 콜백함수

#     #여기는 두개가 있다. signal이 (시작, 종료)
#     @pyqtSlot(int)
#     def recvCnt(self, cnt):
#         self.window.progressBar.setValue(cnt)  # 받아서 화면을 바꿔준다.

#     @pyqtSlot()
#     def onThreadStop(self):# 이미 연결시켜놓음(디자이너에서)
#         if self.threadObj.isRunning():
#             self.threadObj.terminate()
#             # 플래그 변수 등을 활용하여 반복문도 종료되게 처리
#             # 다시 시작하고 싶으면
#             # self.threadObj.wait()            
#             # self.threadObj.start()    
        

#     #쓰레드 걸기
#     #쓰레드 도는동안에 

# # 쓰레드(프로세스를 잘게 쪼개면 쓰레드가 된다.) 객체
# class Worker(QObject):
#     # 시그널 담당 객체
#     signal_obj = pyqtSignal(int)  # 전에는 디자이너 내에서 해줫음.#int는 1,2,3...
#     def __init__(self, parent=None):
#         super(self.__class__, self).__init__(parent)

#     @pyqtSlot()
#     def start(self):# 자바의 Thread의 run() 메소드
#         #0~100까지 계속해서 반복!! 숫자를 생성해서 이벤트를 발생
#         cnt = 0
#         while cnt < 100: #<- 쓰레드 단위로 쪼개줘야 따로 돈다.
#             cnt += 1
#             if cnt >= 100:
#                 cnt = 0
            
#             time.sleep(0.1)

#             # 숫자를 증가하면서 시그널(이벤트)을 계속 발생
#             self.signal_obj.emit(cnt)  # emit -> 이벤트 발동 함수





    

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    #print(sys.argv)
    #Worker() ##__class__ => '__main__.Worker()'
    MainWin()
    
    app.exec_() # 그냥 닫으면 프로세스에 남아 있따.
    sys.exit(0)