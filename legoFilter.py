#!/usr/bin/python

from PIL import Image
from numpy import *
from imageTools import grey
import sys
import os

class LegoFilter():
    def __init__(self):
        if len(sys.argv) == 2:
            self.modelSize = 39
        else:
            self.modelSize = int(sys.argv[2])
        self.distImgFile = sys.argv[1]
        if self.modelSize <= 0:
            print("Expect a positive number!")
            exit(0)
        if not os.path.exists(self.distImgFile):
            print("Input the image name you want to cover a filer!")
        self.modelImgFile = 'ori.png'
        fullModelImgObj = grey(Image.open(self.modelImgFile).convert('RGBA'))
        self.modelImgObj = fullModelImgObj.crop((0, 0, fullModelImgObj.size[0]//2, fullModelImgObj.size[1]//2))
        self.modelImgObj = self.modelImgObj.resize((self.modelSize, self.modelSize), Image.ANTIALIAS)
        self.modelWidth = self.modelImgObj.size[0]
        self.modelHeight = self.modelImgObj.size[1]
        self.modelPixdata = self.modelImgObj.load()
        self.centerColor =  self.modelPixdata[self.modelWidth - 1, self.modelHeight - 1]
        self.borderDict = {}
        for i in range(self.modelWidth//40 + 1):
            self.borderDict[i] = (-20, -20, -20, 0)
            self.borderDict[self.modelWidth - (i+1)] = (20, 20, 20, 0)
    def single2Img(self, a, b):
        avgColor = (0, 0, 0, 0)
        for x in range(self.modelWidth):
            for y in range(self.modelHeight):
                avgColor = tuple(self.distImgPixData[x+self.modelWidth*a, y+self.modelHeight*b][i] + avgColor[i] for i in range(4))
        avgColor = tuple(int(avgColor[i]/(self.modelWidth*self.modelHeight)) for i in range(4))
        for x in range(self.modelWidth):
            for y in range(self.modelHeight):
                self.distImgPixData[x+self.modelWidth*a, y+self.modelHeight*b] = tuple(avgColor[i] + \
                self.modelPixdata[x, y][i] - self.centerColor[i] + self.borderDict.get(x, (0,0,0,0))[i]\
                - self.borderDict.get(y, (0,0,0,0))[i] for i in range(4))
    def apply2Img(self):
        self.distImgObj = Image.open(self.distImgFile).convert('RGBA')
        self.distImgPixData = self.distImgObj.load()
        self.distImgWidth = self.distImgObj.size[0]
        self.distImgHeight = self.distImgObj.size[1]
        numX = int(self.distImgWidth/self.modelWidth)
        numY = int(self.distImgHeight/self.modelHeight)
        for i in range(numX):
            for j in range(numY):
                self.single2Img(i, j)
        self.distImgObj = self.distImgObj.crop((0, 0, numX*self.modelWidth, numY*self.modelHeight))
        self.distImgObj.save('dist.png')


if __name__ == '__main__':
    legoFilter = LegoFilter()
    legoFilter.apply2Img()
