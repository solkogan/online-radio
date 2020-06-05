import sys, time, threading
# pip install python-vlc
# (нужно также установить программу VLC плеер)
# Если у вас python 3.8 и выше то пропатчите файл vlc.py если есть ошибки при запуске
import vlc
# Импортируем наш интерфейс
from guiradio import *
from PyQt5 import QtCore, QtGui, QtWidgets

# Список каналов
canals=[]
# переменная останавливающая проигрывание музыки
songflag=0

# Отдельный поток - обёртка
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper

# Поток включающий музыку
@thread
def playradio(canal):
    global songflag
    songflag=1
    ppp = vlc.MediaPlayer(canal)
    ppp.play()
    # Радио играет пока переменная songflag не станет равна нулю 
    while songflag==1:
        time.sleep(0.7)
    ppp.stop()

# Графический интерфейс PyQT
class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        global canals
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Читаем список каналов из файла radiochannels.txt
        f=open('radiochannels.txt','r',encoding='UTF-8')
        for x in f:
            mas=x.split('|')
            name=mas[0]
            # Добавляем названия каналов в listView
            self.ui.listView.addItem(name)
            canal=mas[1]
            # Добавляем имя и ссылку на канал в список canals
            canals.append(x)
        # Здесь прописываем события нажатий на кнопки и listView                     
        self.ui.pushButton.clicked.connect(self.PlayMusic)
        self.ui.pushButton_2.clicked.connect(self.StopMusic)
        self.ui.listView.currentTextChanged.connect(self.PlayMusic)

    # Запуск звучания                  
    def PlayMusic(self):
        global songflag
        songflag=0
        time.sleep(1)
        # Получаем имя выбранного в списке канала
        name=self.ui.listView.currentItem().text()
        for x in canals:
            # Ищем выбранное имя канала в списке каналов
            if name in x:
                mas=x.split('|')
                # Получаем ссылку на поток вещания
                canal=mas[1].strip()
                print(name)
                # Включаем проигрывание музыки
                playradio(canal)
                
    # Функция остановки звучания
    def StopMusic(self):
        global songflag
        # Обнуляем переменную отвечающую за выключение плеера
        songflag=0
        time.sleep(1)
        
    # При выходе сперва нужно остановить звучание
    def closeEvent(self, event):
        StopMusic()
        event.accept()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
