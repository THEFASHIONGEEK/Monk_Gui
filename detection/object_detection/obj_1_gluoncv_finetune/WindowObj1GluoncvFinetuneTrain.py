import os
import sys
import json
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class WindowObj1GluoncvFinetuneTrain(QtWidgets.QWidget):

    backward_hyper_param = QtCore.pyqtSignal();
    forward_1_gluoncv_finetune = QtCore.pyqtSignal(); 

    def __init__(self):
        super().__init__()
        self.title = 'GluonCV Finetune - Train'
        self.left = 100
        self.top = 100
        self.width = 900
        self.height = 600
        self.load_cfg();
        self.initUI()

    def load_cfg(self):
        if(os.path.isfile("obj_1_gluoncv_finetune.json")):
            with open('obj_1_gluoncv_finetune.json') as json_file:
                self.system = json.load(json_file)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height);



        # Backward
        self.b1 = QPushButton('Back', self)
        self.b1.move(700,550)
        self.b1.clicked.connect(self.backward)

        # Quit
        self.b2 = QPushButton('Quit', self)
        self.b2.move(800,550)
        self.b2.clicked.connect(self.close)


        self.tb1 = QTextEdit(self)
        self.tb1.move(20, 20)
        self.tb1.resize(400, 250)
        self.tb1.setText(self.get_params());
        self.tb1.setReadOnly(True)


        self.l1 = QLabel(self);
        self.l1.setText("Num Epochs: ");
        self.l1.move(20, 300);

        self.e1 = QLineEdit(self)
        self.e1.move(120, 300);
        self.e1.setText(self.system["epochs"]);
        self.e1.resize(200, 25);


        self.l2 = QLabel(self);
        self.l2.setText("Saved Model Name: ");
        self.l2.move(20, 350);

        self.e2 = QLineEdit(self)
        self.e2.move(170, 350);
        self.e2.setText(self.system["output_model_name"]);
        self.e2.resize(200, 25);


        # Train
        self.b3 = QPushButton('Train', self)
        self.b3.move(20, 450)
        self.b3.clicked.connect(self.train)


        # Stop 
        self.b4 = QPushButton('Stop', self)
        self.b4.move(150, 450)
        self.b4.clicked.connect(self.stop)


        # Infer 
        self.b4 = QPushButton('Infer', self)
        self.b4.move(250, 450)
        self.b4.clicked.connect(self.forward)


        self.te1 = QTextBrowser(self);
        self.te1.move(450, 20);
        self.te1.setFixedSize(400, 500);


        self.l3 = QLabel(self);
        self.l3.setText("Status: ");
        self.l3.move(420, 550);

        self.tb2 = QTextEdit(self)
        self.tb2.move(470, 550)
        self.tb2.resize(200, 25)
        self.tb2.setText("Not Started");
        self.tb2.setReadOnly(True)


        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)





    def get_params(self):
        wr = "";
        wr += "Anno Type -  {}\n".format(self.system["anno_type"]);
        wr += "Root Dir -   {}\n".format(self.system["root_dir"]);
        if(self.system["anno_type"] == "monk"):
            wr += "Anno Dir -   {}\n".format(self.system["anno_dir"]);
        else:
            wr += "Anno File -  {}\n".format(self.system["anno_file"]);
        wr += "Model -  {}\n".format(self.system["model"]);
        wr += "Pretrained - {}\n".format(self.system["use_pretrained"]);
        wr += "GPU -        {}\n".format(self.system["use_gpu"]);
        if(self.system["use_gpu"]):
            wr += "Devices -    {}\n".format(self.system["devices"]);

        return wr;




    def train(self):
        self.te1.setText("");
        self.tb2.setText("Running");
        self.system["epochs"] = self.e1.text();
        self.system["output_model_name"] = self.e2.text();

        with open('obj_1_gluoncv_finetune.json', 'w') as outfile:
            json.dump(self.system, outfile);

        os.system("cp cfg/detection/object_detection/obj_1_gluoncv_finetune/train_obj_1_gluoncv_finetune.py .");
        os.system("cp cfg/detection/object_detection/obj_1_gluoncv_finetune/train_obj_1_gluoncv_finetune.sh .");


        self.process.start('bash', ['train_obj_1_gluoncv_finetune.sh'])
        self.append("Process PID: " + str(self.process.pid()) + "\n");


    def stop(self):
        self.tb2.setText("Interrupted");
        QMessageBox.about(self, "Training Status", "Interrupted");
        self.process.kill();
        self.append("Training Stopped\n")


    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        if("Completed" in text):
            QMessageBox.about(self, "Training Status", "Completed");
            self.tb2.setText("Completed");
        if("Error" in text or "error" in text or "ImportError" in text):
            self.tb2.setText("Errors Found");
        self.append(text)


    def stderrReady(self):
        text = str(self.process.readAllStandardError().data(), encoding='utf-8')
        QMessageBox.about(self, "Training Status", "Errors Found");
        self.tb2.setText("Errors Found");
        self.append(text)


    def append(self, text):
        cursor = self.te1.textCursor()  
        self.te1.ensureCursorVisible() 
        cursor.movePosition(cursor.End)
        cursor.insertText(text)        


    def forward(self):
        self.forward_1_gluoncv_finetune.emit();

    def backward(self):
        self.backward_hyper_param.emit();


'''
app = QApplication(sys.argv)
screen = WindowObj1GluoncvFinetuneTrain()
screen.show()
sys.exit(app.exec_())
'''