#!/home/emilia/anaconda3/bin/ipython
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:17:21 2015

@author: emilia
"""

import textwrap
import qdarkstyle
import sys
from PyQt4 import QtGui, QtCore
import os
from Options import *

class HelpWindow(QtGui.QWidget):
    def __init__(self):
        
        super(HelpWindow, self).__init__()
        self.initHelp()
        
    def initHelp(self):
        
        self.designValue = "Fairstyle"
        tab1 = QtGui.QTabWidget
        
        self.textAbout = u'In this game player slides numbered tiles on a grid \n\
        to combine them and create a tile with the number \n\
        2048. Please, read the README file in order\n\
        to get further instructions.'
        
        self.setGeometry(300, 300, 400, 350)
        self.setWindowTitle("Help")
        #self.show()
        
    def paintEvent(self, event):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
        
    def drawText(self, event, qp):
        
        qp.setPen(QtGui.QColor(168,34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.textAbout)
       
       
    def setDesign(self):
        
        if self.designValue == "Fairstyle":
            self.setStyleSheet('plastique')
        elif self.designValue == "Darkstyle":
            self.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
###########################################################################        
def main():

    app = QtGui.QApplication(sys.argv)
    
    ex = HelpWindow()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
