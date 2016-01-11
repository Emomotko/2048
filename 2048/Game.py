#!/home/emilia/anaconda3/bin/ipython
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:13:52 2015

@author: emilia
"""


import qdarkstyle
import numpy as np
import sys
from PyQt4 import QtGui, QtCore
import os
import itertools

class Tile(object):
    
    def __init__(self, n, k):
        super(Tile, self).__init__()
        
        self.initTile(n, k)
        
    def initTile(self, n, k):
        
        self.score = 0
        self.tableMain = np.zeros((n, n))   
        self.generateInitialValues(n, k)
        self.winning_indicator = False
        
    
    def updateValues(self, wArrow, n, k=0):
        
        tableResult = self.tableMain.copy()
        a = np.zeros((n, n))
        K = np.repeat(False, n*n)
        K.shape = (n, n)
        while(not np.array_equal(a, tableResult)):
            a = tableResult.copy()
            if wArrow == "d":
                for i in np.arange(n-1, -1, -1):
                    for j in np.arange(0, n):
                        if i != 0:
                            if (tableResult[i-1, j] == tableResult[i, j] and tableResult[i, j] != -1 and np.all(K[0:i+1, j] == False)) or ( tableResult[i-1, j] == 0 or tableResult[i, j] == 0):                                
                                if tableResult[i-1, j] == tableResult[i, j] and tableResult[i, j] != 0:
                                    self.score = self.score + 2*tableResult[i, j]
                                    K[i, j] = True
                                tableResult[i, j] = tableResult[i, j] + tableResult[i-1, j]                                
                                tableResult[i-1, j] = 0
                                
            elif  wArrow == "u":
                for i in np.arange(0, n):
                    for j in np.arange(0, n):
                        if i != n-1:
                            if (tableResult[i+1, j] == tableResult[i, j] and tableResult[i, j] != -1 and np.all(K[i:n, j] == False)) or (tableResult[i+1, j] == 0 or tableResult[i, j] == 0):
                                if tableResult[i+1, j] == tableResult[i, j] and tableResult[i, j] != 0:
                                    self.score = self.score + 2*tableResult[i, j]
                                    K[i, j] == True
                                tableResult[i, j] = tableResult[i, j] + tableResult[i+1, j]
                                tableResult[i+1, j] = 0
            elif wArrow == "l":
                for i in np.arange(0, n):
                    for j in np.arange(0, n):
                        if j!= n - 1:
                            if (tableResult[i, j+1] == tableResult[i, j] and tableResult[i, j] != -1 and np.all(K[i, j:n] == False)) or (tableResult[i, j+1] == 0 or tableResult[i, j] == 0):
                                if tableResult[i, j+1] == tableResult[i, j] and tableResult[i, j] != 0:
                                    self.score = self.score + 2*tableResult[i, j]
                                    K[i, j] = True
                                tableResult[i, j] = tableResult[i, j] + tableResult[i, j+1]
                                tableResult[i, j+1] = 0
            elif wArrow == "r":
                for i in np.arange(0, n):
                    for j in np.arange(n-1, -1, -1):
                        if j!= 0:
                            if (tableResult[i, j-1] == tableResult[i, j] and tableResult[i, j] != -1 and np.all(K[i, 0:j+1] == False)) or (tableResult[i, j-1] == 0 or tableResult[i, j] == 0):
                                if tableResult[i, j-1] == tableResult[i, j] and tableResult[i, j] != 0:
                                    self.score = self.score + 2*tableResult[i, j]
                                    K[i, j] = True
                                tableResult[i, j] = tableResult[i, j] + tableResult[i, j-1]
                                tableResult[i, j-1] = 0
                                
        if 2048 in tableResult:
            self.tableMain = tableResult
            self.winning_indicator= True
            print("WINNER!!!")
        noValues = np.where(tableResult == 0)
        if len(noValues[0]) >= 1 and  not np.array_equal(self.tableMain, tableResult):
            indexX = np.random.random_integers(0, len(noValues[0])-1)
            x = noValues[0][indexX]
            y = noValues[1][indexX]
            tableResult[x, y] = 2  
        self.tableMain = tableResult    
        
                
    def generateInitialValues(self, n, k=0):
        
        x_y = np.array(list(itertools.product(range(0, n),range(0, n))))
        p = np.random.choice(range(0, len(x_y)), size = 2 + k, replace = False)
        vertices = x_y[p]
        
        x = vertices[0:2, 0]
        y = vertices[0:2, 1]
        
        if (x[0] != x[1]) or (y[0] != y[1]):
            values = np.random.choice([2,4], 2, replace = True)
            self.tableMain[x[0], y[0]] = values[0]
            self.tableMain[x[1], y[1]] = values[1]
        else: 
            values = np.random.choice([2,4], 1, replace = True)
            self.tableMain[x, y] = values
            
        if k >= 1:
            x_k = vertices[2:2+k, 0]
            y_k = vertices[2:2+k, 1]
            for i in range(0, k):
                self.tableMain[x_k[i], y_k[i]] = -1
            

