#-*-coding:utf-8-*-
import sys
import numpy as np
from math import sin, cos, pi, radians
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MyApp(QMainWindow): #Main Window

    def __init__(self):
        super().__init__()
        wg = MainWidget()
        self.setCentralWidget(wg)
        self.initUI()

    def initUI(self):

        #Basic Settings
        self.setWindowTitle("이중슬릿 모의실험 by.30712_오명진")
        self.setWindowIcon(QIcon('resources//icon.png'))

        self.show()

class MainWidget(QWidget): #MainWidget


    def __init__(self):
        super().__init__()

        self.Theta = 0.1
        self.Lambda = 0.1
        self.a = 0.1
        self.d = 0.1

        self.initUI()

    def initUI(self):

        # Creating Objects
        self.bar1 = QSlider(Qt.Horizontal) # Theta
        self.bar1.setRange(1, 900) #Original Value *= 10
        self.bar1.setSingleStep(1)
        self.bar1.setValue(1)
        self.dis1 = QLabel("0.1")

        self.bar2 = QSlider(Qt.Horizontal) # Lambda
        self.bar2.setRange(1000, 9000)
        self.bar2.setSingleStep(10)
        self.bar2.setValue(1000)
        self.dis2 = QLabel("1000")

        self.bar3 = QSlider(Qt.Horizontal) # a
        self.bar3.setRange(1, 50) #Original Value *= 100
        self.bar3.setSingleStep(1)
        self.bar3.setValue(1)
        self.dis3 = QLabel("0.01")

        self.bar4 = QSlider(Qt.Horizontal) # d
        self.bar4.setRange(1, 100) #Original Value *= 100
        self.bar4.setSingleStep(1)
        self.bar4.setValue(1)
        self.dis4 = QLabel("0.01")

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.VChanged()


        #Grid Layout
        grid = QGridLayout()
        grid.addWidget(QLabel('스크롤 바를 움직여 값을 지정하세요'), 0, 1)
        grid.addWidget(QLabel('값'), 0, 2)
        grid.addWidget(QLabel('단위'), 0, 3)

        grid.addWidget(QLabel('표시 각 범위(x축)'), 1, 0)
        grid.addWidget(self.bar1, 1, 1)
        grid.addWidget(self.dis1, 1, 2)
        grid.addWidget(QLabel('±θ(deg)'), 1, 3)

        grid.addWidget(QLabel('파장'), 2, 0)
        grid.addWidget(self.bar2, 2, 1)
        grid.addWidget(self.dis2, 2, 2)
        grid.addWidget(QLabel('λ(nm)'), 2, 3)

        grid.addWidget(QLabel('슬릿의 폭'), 3, 0)
        grid.addWidget(self.bar3, 3, 1)
        grid.addWidget(self.dis3, 3, 2)
        grid.addWidget(QLabel('a(nm)'), 3, 3)

        grid.addWidget(QLabel('슬릿 중심 사이의 간격'), 4, 0)
        grid.addWidget(self.bar4, 4, 1)
        grid.addWidget(self.dis4, 4, 2)
        grid.addWidget(QLabel('d(nm)'), 4, 3)


        #Event Handling

        self.bar1.valueChanged.connect(self.VChanged)
        self.bar2.valueChanged.connect(self.VChanged)
        self.bar3.valueChanged.connect(self.VChanged)
        self.bar4.valueChanged.connect(self.VChanged)


        # Vertical Layout
        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addWidget(self.canvas)

        self.setLayout(vbox)

    #Event Methods
    def VChanged(self):
        try:
            self.bar1Changed()
            self.bar2Changed()
            self.bar3Changed()
            self.bar4Changed()
            self.drawGraph()
        except:
            pass

    def bar1Changed(self):
        self.dis1.setText(str(self.bar1.value()/10))
        self.Theta = self.bar1.value()/10

    def bar2Changed(self):
        self.dis2.setText(str(self.bar2.value()))
        self.Lambda = self.bar2.value()/1000000000

    def bar3Changed(self):
        self.dis3.setText(str(self.bar3.value()/100))
        self.a = self.bar3.value() / 100000

    def bar4Changed(self):
        self.dis4.setText(str(self.bar4.value()/100))
        self.d = self.bar4.value() / 100000

    def drawGraph(self):
        self.fig.clf()
        graph = self.fig.add_subplot(111)
        alpha = lambda x : ((self.a)*pi/(self.Lambda)*sin(radians(x)))
        beta = lambda x : ((pi*(self.d)/(self.Lambda))*sin(x))
        x = np.arange(-(self.Theta), self.Theta, 0.001)
        y = [(sin(alpha(v))/(alpha(v))*cos(beta(v))*cos(beta(v))) for v in x]
        graph.plot(x,y, color = 'springgreen')
        graph.axis([None, None, 0, 1.2])
        self.canvas.draw()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
