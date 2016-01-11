#!/home/emilia/anaconda3/bin/ipython
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:15:40 2015

@author: emilia
"""

import qdarkstyle
import sys
from PyQt4 import QtGui, QtCore
import os


class OptionWindow(QtGui.QWidget):
    
    def __init__(self):
        
        super(OptionWindow, self).__init__()
        self.initOption()
        
    def initOption(self):
        
        tabs = QtGui.QTabWidget(self)
        tabs.resize(390, 280)
        
        tab1 = QtGui.QWidget()
        self.vbox1 = QtGui.QVBoxLayout()
            
        ###########################################
        
        self.apply = QtGui.QPushButton("Apply", self)
        self.apply.setGeometry(160, 290, 70, 30)
        
        ############ Difficulty level #############
        
        self.difLevel = RadioButtonsGroup()
        self.difLevel2 = self.difLevel.groupRadio
        
        self.difLevelValue = 0
        
        self.difLevel.easy.clicked.connect(self.setDif)
        self.difLevel.medium.clicked.connect(self.setDif)
        self.difLevel.hard.clicked.connect(self.setDif)
        self.a = "Easy"
        self.difLabel = QtGui.QLabel("The difficulty level is Easy and the height of the plane is 4. No additional dummy tiles will appear.")
        self.difLabel.setWordWrap(True)
        ###########################################
        
        self.lbTiles = QtGui.QLabel("Please, choose the height of the plane:")
        self.tilesSpinBox = QtGui.QDoubleSpinBox()
        self.tilesSpinBox.setRange(4, 8)
        self.tilesSpinBox.setDecimals(0)
        self.n = 4
        self.tilesSpinBox.valueChanged.connect(self.computeN)
        
        ################## Style ##################
        
        designLabel = QtGui.QLabel("What style of the application do you prefer?")
        self.designWidgetParent = RadioButtonsGroupDesign()
        self.designWidget = self.designWidgetParent.groupRadioDesign
        self.designValue = "Fairstyle"
        
        ###########################################
        self.apply.clicked.connect(self.setDesign)
        self.apply.clicked.connect(self.close)
        
        self.vbox1.addWidget(self.lbTiles)
        self.vbox1.addWidget(self.tilesSpinBox)
        self.vbox1.addWidget(self.difLevel2)
        self.vbox1.addWidget(self.difLabel)
#             
        tab1.setLayout(self.vbox1)
        tabs.addTab(tab1, "Difficulty")
        
        tab2 = QtGui.QWidget()
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(designLabel)
        vbox2.addWidget(self.designWidget)
        tab2.setLayout(vbox2)
        tabs.addTab(tab2, "Design")
        
        self.setGeometry(300, 300, 400, 330)
        self.setWindowTitle("Options")
        #self.show()
        
    def computeN(self):
        self.n = int(self.tilesSpinBox.value())
        self.difLabel.setText("The difficulty level is " + self.a + " and the height if the plane is " + str(self.n)+ 
        "."+ " There will be "+ str(self.difLevelValue)+ " additional dumy tiles.")

    def setDif(self):
        
        sender = self.sender()
        self.a = sender.text()
        if sender.text() == "Easy":
            self.difLevelValue = 0
        elif sender.text() == "Medium" and (self.n == 4 or self.n == 5):
            self.difLevelValue = 1
        elif sender.text() == "Medium" and (self.n == 6 or self.n == 7 or self.n == 8):
            self.difLevelValue = 2
        elif sender.text() == "Hard" and (self.n == 4 or self.n == 5):
            self.difLevelValue = 2
        elif sender.text() == "Hard" and (self.n == 6 or self.n == 7):
            self.difLevelValue = 3
        elif sender.text() == "Hard" and (self.n == 8):
            self.difLevelValue = 4
        self.difLabel.setText("The difficulty level is " + sender.text() + " and the height if the plane is " + str(self.n)+ 
        "."+ " There will be "+ str(self.difLevelValue)+ " additional dumy tiles.")
        

    def setDesign(self):
        
        if self.designWidgetParent.whichChosen() == "Fairstyle":
            self.designValue = "Fairstyle"
            self.setStyleSheet('plastique')
        elif self.designWidgetParent.whichChosen() == "Darkstyle":
            self.designValue = "Darkstyle"
            self.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

        
######################################################    

class RadioButtonsGroup(QtGui.QWidget):
    
    def __init__(self):
        
        super(RadioButtonsGroup, self).__init__();
        self.initRadio()
                 
    def initRadio(self):
        
        radioLayout = QtGui.QVBoxLayout()
        radioLayout.addStretch(1)
        self.groupRadio = QtGui.QGroupBox()
        
        self.easy = QtGui.QRadioButton("Easy")
        self.medium = QtGui.QRadioButton("Medium")
        self.hard = QtGui.QRadioButton("Hard")
        self.easy.setChecked(True)
        
        radioLayout.addWidget(self.easy)
        radioLayout.addWidget(self.medium)
        radioLayout.addWidget(self.hard)
        
        self.groupRadio.setLayout(radioLayout)
        
        self.whichChecked = "Easy"
        
    def whichChosen(self):
        
        if self.easy.isChecked(): return("Easy")
        elif self.medium.isChecked(): return("Medium")
        elif self.hard.isChecked(): return("Hard")
        
        
class RadioButtonsGroupDesign(QtGui.QWidget):
    
    def __init__(self):
        
        super(RadioButtonsGroupDesign, self).__init__();
        self.initRadioDesign()
                 
    def initRadioDesign(self):
        
        radioLayout = QtGui.QHBoxLayout()

        self.groupRadioDesign = QtGui.QGroupBox()
        self.dark = QtGui.QRadioButton("Darkstyle")
        self.fair = QtGui.QRadioButton("Fairstyle")
        self.fair.setChecked(True)
        
        radioLayout.addWidget(self.dark)
        radioLayout.addWidget(self.fair)
        
        self.groupRadioDesign.setLayout(radioLayout)
        
    def whichChosen(self):
        
        if self.dark.isChecked(): return("Darkstyle")
        elif self.fair.isChecked(): return("Fairstyle")

###################################################### 

def main():

    app = QtGui.QApplication(sys.argv)
    
    ex = OptionWindow()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
