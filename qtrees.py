import numpy as np
import pygame as pg

class quadtree(object):
    QUANTITY=10
    DIV=2
    SURFACE = pg.Surface((10,10))  # pylint: disable=too-many-function-args
    def __init__(self,x1,y1,x2,y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.children=[]
        self.visible=True
        self.color1=(0,50,0)
        self.color2=(0,255,0)
        self.colorr=(255,255,255)
        self.drawlines=True
        self.mine=[]

    def construct(self,basearray):
        count =0
        for i in basearray:
            if  ((i.x>=self.x1) and (i.x<=self.x2) and (i.y>=self.y1) and (i.y<=self.y2)):
                count+=1
                self.mine.append(i)
        if count>quadtree.QUANTITY:
            self.visible=False
            width=self.x2-self.x1
            height = self.y2-self.y1
            if width > 2 and height > 2:
                for i in range(quadtree.DIV):
                    for j in range(quadtree.DIV):
                        x1 = self.x1 + width*i/quadtree.DIV
                        x2 = x1+width/quadtree.DIV
                        y1 = self.y1 + height*j/quadtree.DIV
                        y2 = y1 + height/quadtree.DIV
                        #print(x1,y1,x2,y2)
                        temp = quadtree(x1,y1,x2,y2)
                        self.children.append(temp)
                        temp.construct(self.mine)
        if(count==quadtree.QUANTITY):
            self.colorr=self.color2
        if(count<quadtree.QUANTITY and count>0):
            self.colorr=self.color1
        if count == 0:
            self.visible=False
        


    def draw(self):
        if self.visible:
            rrect = pg.Rect(int(self.x1),int(self.y1),int(self.x2-self.x1),int(self.y2-self.y1))
            pg.draw.rect(quadtree.SURFACE,self.colorr,rrect,1)
            centerx = (self.x1+self.x2)/2
            centery = (self.y1 + self.y2)/2
            if  self.drawlines:
                for i in self.mine:
                    pg.draw.line(quadtree.SURFACE,self.colorr,(int(centerx),int(centery)),(int(i.x),int(i.y)))

    def recursifdraw(self):
        self.draw()
        for i in self.children:
            i.recursifdraw()