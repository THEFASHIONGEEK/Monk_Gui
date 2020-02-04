import os
import sys
import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class WindowObj4EfficientdetHyperParam(QtWidgets.QWidget):

    backward_model_param = QtCore.pyqtSignal();
    forward_train = QtCore.pyqtSignal();

    def __init__(self):
        super().__init__()
        self.title = 'Efficient Detection - Hyper Param'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 220
        self.load_cfg();
        self.initUI()


    def load_cfg(self):
        if(os.path.isfile("obj_4_efficientdet.json")):
            with open('obj_4_efficientdet.json') as json_file:
                self.system = json.load(json_file)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height);

        # Forward
        self.b1 = QPushButton('Next', self)
        self.b1.move(300,180)
        self.b1.clicked.connect(self.forward)

        # Backward
        self.b2 = QPushButton('Back', self)
        self.b2.move(200,180)
        self.b2.clicked.connect(self.backward)


        # Quit
        self.b3 = QPushButton('Quit', self)
        self.b3.move(400,180)
        self.b3.clicked.connect(self.close)


        self.l1 = QLabel(self);
        self.l1.setText("1. learning_rate:");
        self.l1.move(20, 20);

        self.e1 = QLineEdit(self)
        self.e1.move(150, 20);
        self.e1.setText(self.system["lr"]);
        self.e1.resize(200, 25);



        self.l3 = QLabel(self);
        self.l3.setText("2. es_min_delta:");
        self.l3.move(20,70);

        self.e3 = QLineEdit(self)
        self.e3.move(150, 70);
        self.e3.setText(self.system["es_min_delta"]);


        self.l4 = QLabel(self);
        self.l4.setText("3. es_patience:");
        self.l4.move(20, 110);

        self.e4 = QLineEdit(self)
        self.e4.move(150, 110);
        self.e4.setText(self.system["es_patience"]);




    def forward(self):
        self.system["lr"] = self.e1.text();
        self.system["es_min_delta"] = self.e3.text();
        self.system["es_patience"] = self.e4.text();

        with open('obj_4_efficientdet.json', 'w') as outfile:
            json.dump(self.system, outfile)

        self.forward_train.emit();

    def backward(self):
        self.system["lr"] = self.e1.text();
        self.system["es_min_delta"] = self.e3.text();
        self.system["es_patience"] = self.e4.text();

        with open('obj_4_efficientdet.json', 'w') as outfile:
            json.dump(self.system, outfile)
        
        self.backward_model_param.emit();


'''
app = QApplication(sys.argv)
screen = WindowObj4EfficientdetHyperParam()
screen.show()
sys.exit(app.exec_())
'''