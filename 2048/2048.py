#!/home/emilia/anaconda3/bin/ipython
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:18:03 2015

@author: emilia
"""


import qdarkstyle
import sys
from PyQt4 import QtGui, QtCore
import os
from Help import *
from Options import *
from Game import *

class FirstWindow(QtGui.QMainWindow):
    
    def __init__(self):
        
        super(FirstWindow, self).__init__()
        self.initUi()
        
        
    def initUi(self):
        
        self.form_widget = FormWidget(self) 
        self.op = OptionWindow()
        self.n = self.op.n
        self.ab = HelpWindow()
        self.gameAll = Game(self)
        self.gameAll.hide()
        self.setCentralWidget(self.form_widget)
        self.msgBox = QtGui.QMessageBox(self)
        
        self.op.apply.clicked.connect(self.applyChanges)
        
        self.form_widget.startButton.clicked.connect(self.startGame)
        
        self.designValue = "Fairstyle"
        
        self.k = 0
        self.gameAll.exitButton.clicked.connect(self.close_all)
        
        optionAction = QtGui.QAction(QtGui.QIcon('rys.png'), 'Options', self)
        exitAction = QtGui.QAction(QtGui.QIcon('rys.png'), 'Exit', self)
        aboutAction = QtGui.QAction(QtGui.QIcon('rys.png'), 'About', self)
        
        exitAction.triggered.connect(self.close_all)
        optionAction.triggered.connect(self.open_options)
        aboutAction.triggered.connect(self.open_about)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(optionAction)
        fileMenu.addAction(exitAction)
        
        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(aboutAction)
        
        self.setGeometry(300, 300, 650, 650)
        self.setWindowTitle("Main window")
        self.show()
        
    def applyChanges(self):
        
        self.n = int(self.op.tilesSpinBox.value())
        
        self.gameAll.n = self.n
        
        if self.op.difLevel.whichChosen() == "Easy":
            self.k = 0
        elif self.op.difLevel.whichChosen() == "Medium" and (self.n == 4 or self.n == 5):
            self.k = 1
        elif self.op.difLevel.whichChosen() == "Medium" and (self.n == 6 or self.n == 7 or self.n == 8):
            self.k = 2
        elif self.op.difLevel.whichChosen() == "Hard" and (self.n == 4 or self.n == 5):
            self.k = 2
        elif self.op.difLevel.whichChosen() == "Hard" and (self.n == 6 or self.n == 7):
            self.k = 3
        elif self.op.difLevel.whichChosen() == "Hard" and (self.n == 8):
            self.k = 4
            
        
        self.gameAll.k = self.k
        self.gameAll.tiles = Tile(self.gameAll.n, self.gameAll.k)
        self.gameAll.coords = self.gameAll.findCoords()
        self.gameAll.coordsT = self.gameAll.findCoordsText()
        
        if self.op.designWidgetParent.whichChosen() == "Fairstyle":
            self.designValue = "Fairstyle"
            self.setStyleSheet('plastique')
        elif self.op.designWidgetParent.whichChosen() == "Darkstyle":
            self.designValue = "Darkstyle"
            self.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
        self.ab.designValue = self.op.designWidgetParent.whichChosen()
        self.ab.setDesign()
        self.gameAll.designValue = self.op.designWidgetParent.whichChosen()
        self.gameAll.setDesign()
        self.gameAll.scoreDisplay.display(self.gameAll.tiles.score)
        
    def open_options(self):
        self.op.show()
  
    def open_about(self):
        self.ab.show()
        
    def setDesign(self):
        
        sender = self.sender()
        if sender.text() == "Fairstyle":
            self.designValue = "Fairstyle"
            self.setStyleSheet('plastique')
        elif sender.text() == "Darkstyle":
            self.designValue = "Darkstyle"
            self.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
        self.ab.setDesign()
        
    def startGame(self):
        self.form_widget.hide()
        self.setCentralWidget(self.gameAll)
        self.gameAll.show()


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_B:
            e.accept()
            self.key = "d"
            self.gameAll.tiles.updateValues(self.key, self.n)
            self.gameAll.update()          
        elif e.key() == QtCore.Qt.Key_Y:
            self.key = "u"
            self.gameAll.tiles.updateValues(self.key, self.n)
            self.gameAll.update()
        elif e.key() == QtCore.Qt.Key_G:
            self.key = "l"
            self.gameAll.tiles.updateValues(self.key, self.n)
            self.gameAll.update()
        elif e.key() == QtCore.Qt.Key_H:
            self.key = "r" 
            self.gameAll.tiles.updateValues(self.key, self.n)
            self.gameAll.update()
        elif e.key() == QtCore.Qt.Key_S:
            self.gameAll.tiles.winning_indicator = False
            self.gameAll.tiles.initTile(self.n, self.k)
            self.gameAll.update()
            self.gameAll.scoreDisplay.display(self.gameAll.tiles.score)
        self.gameAll.scoreDisplay.display(self.gameAll.tiles.score)
        
    def close_all(self):
        self.close()
        self.op.close()
        self.ab.close()
        
       
                
    def keyReleaseEvent(self, e):
         if self.gameAll.tiles.winning_indicator == True:
            
            a = QtGui.QMessageBox(self)
            reply = a.question(self, 'You have won the game.', "Do you want to play again?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                a.close()
                self.gameAll.tiles.winning_indicator = False
                self.gameAll.tiles.initTile(self.n, self.k)
                self.gameAll.update()
                self.gameAll.scoreDisplay.display(self.gameAll.tiles.score)
            else:
                self.close()
                self.op.close()
                self.ab.close()
######################################################
        
class FormWidget(QtGui.QWidget):

    def __init__(self, parent):        
        super(FormWidget, self).__init__(parent)
        self.layout = QtGui.QHBoxLayout(self)

        self.startButton = QtGui.QPushButton("Start")
        self.layout.addWidget(self.startButton)
        self.setSizePolicy (QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        

        self.setLayout(self.layout)
        
        
        
class Game(QtGui.QWidget):
    
    def __init__(self, parent):
        
        super(Game, self).__init__(parent)
        self.initGame()

        
    def initGame(self):
        
        self.designValue = "Fairstyle"
        self.n = 4
        self.key = "u"
        self.k = 0
        self.exitButton = QtGui.QPushButton("Exit", self)
        self.exitButton.setGeometry(520, 50, 100, 40)
        self.tiles = Tile(self.n, self.k)
        self.coords = self.findCoords()
        self.coordsT = self.findCoordsText()
        
        self.resize(750, 750)
        
        self.scoreDisplay = QtGui.QLCDNumber(self)
        self.scoreDisplay.setGeometry(520, 400, 100, 80)
     
    def setDesign(self):
        
        if self.designValue == "Fairstyle":
            self.setStyleSheet('plastique')
        elif self.designValue == "Darkstyle":
            self.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
            
     
    def findCoords(self):
        
        coords = []
        for i in range(0, self.n):
            p = []
            for j in range(0, self.n):
                x = i*500/self.n
                y = j*500/self.n
                p.append([x, y])
            coords.append(p)
        return coords
        
    def findCoordsText(self):
        
        coords = []
        for i in range(0, self.n):
            p = []
            for j in range(0, self.n):
                x = i*500/self.n + 500/self.n/2
                y = j*500/self.n + 500/self.n/2
                p.append([x, y])
            coords.append(p)
        return coords
        
    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()   
           
        qp2 = QtGui.QPainter()
        qp2.begin(self)
        self.drawText(e, qp2)
        qp2.end()
        
    def drawRectangles(self, qp):
      
        color = QtGui.QColor(0, 0, 0)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setWidth(3)
        qp.setPen(pen)
    
        qp.setBrush(QtGui.QColor(255, 80, 0, 160))

        colorT = QtGui.QColor(0, 0, 0)
        for i in range(self.n):
            for j in range(self.n):
                if int(self.tiles.tableMain[j, i]) == 0:
                    colorT.setNamedColor("#B0B0B0")
                elif int(self.tiles.tableMain[j, i]) == 2:
                    colorT.setNamedColor("#99FF99")
                elif int(self.tiles.tableMain[j, i]) == 4:
                    colorT.setNamedColor("#CCFF99")
                elif int(self.tiles.tableMain[j, i]) == 8:
                    colorT.setNamedColor("#99FFFF")
                elif int(self.tiles.tableMain[j, i]) == 16:
                    colorT.setNamedColor("#CCCCFF")
                elif int(self.tiles.tableMain[j, i]) == 32:
                    colorT.setNamedColor("#FFCCFF")
                elif int(self.tiles.tableMain[j, i]) == 64:
                    colorT.setNamedColor("#FFFF66")
                elif int(self.tiles.tableMain[j, i]) == 128:
                    colorT.setNamedColor("#99CCFF")
                elif int(self.tiles.tableMain[j, i]) == 256:
                    colorT.setNamedColor("#FF6666")
                elif int(self.tiles.tableMain[j, i]) == 512:
                    colorT.setNamedColor("#FF9933")
                elif int(self.tiles.tableMain[j, i]) == 1024:
                    colorT.setNamedColor("#00FF80")
                elif int(self.tiles.tableMain[j, i]) == 2048:
                    colorT.setNamedColor("#FF3333")  
                elif int(self.tiles.tableMain[j, i]) == -1:
                    colorT.setNamedColor("#000000")
                qp.setBrush(colorT)   
                qp.drawRect(self.coords[i][j][0], self.coords[i][j][1], 500/self.n, 500/self.n)
                
                
    def drawText(self, event, qp):
        
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setFont(QtGui.QFont('Decorative', 17))
        for i in range(self.n):
            for j in range(self.n):
                rect = QtCore.QRect(self.coords[i][j][0], self.coords[i][j][1], 500/self.n, 500/self.n)
                qp.drawText(rect, QtCore.Qt.AlignCenter, str(int(self.tiles.tableMain[j, i])))
         
#####################
    
    
######################################################      
def main():

    app = QtGui.QApplication(sys.argv)
    
    ex = FirstWindow()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
