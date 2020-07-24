import numpy as np
import pygame as pg

WIDTH=100
HEIGHT=100
SWIDTH=100
SHEIGHT = 100

TABLE = []
def init():
    global WIDTH , HEIGHT , TABLE ,SWIDTH,SHEIGHT
    for _i in range(int(SHEIGHT/HEIGHT)):
        row=[]
        for _j in range(int(SWIDTH/WIDTH)):
            row.append([])
        TABLE.append(row)

def get(x,y):
    global WIDTH, HEIGHT,TABLE, SHEIGHT,SWIDTH
    res=[]
    if  x>0 and x<int(SWIDTH/WIDTH) and y>0 and y<int(SHEIGHT/HEIGHT):
        res = TABLE[y][x]
    return res
