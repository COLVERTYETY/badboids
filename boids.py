import pygame as py
import numpy as np
import splintercell

font = "py.font.Font(None, 10)  "

def n(x,y):
    return np.sqrt(x*x+y*y) 

class boid(object):
    SURFACE = py.Surface((10,10))  # pylint: disable=too-many-function-args
    ARRAY=[]
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vx=0
        self.vy=0
        self.ax=0
        self.ay=0
        self.color=(42, 180, 235)
        self.radius=5
        self.vrange=50
        self.maxspeed=5
        self.maxforce=0.5
        self.shape="line"
    
    def apply(self):
        self.vx+=self.ax
        self.vy+=self.ay
        self.ax=0
        self.ay=0
        self.x+=self.vx
        self.y+=self.vy
        (w, h) = boid.SURFACE.get_size()
        self.x=(self.x+w)%w
        self.y=(self.y+h)%h


    def align(self,arr):
        avgvx=0
        avgvy=0
        avgx=0
        avgy=0
        count=0
        repx=0
        repy=0
        repc=0
        for i in arr:
            if isinstance(i,boid) and i is not self:
                distance = (i.x-self.x)*(i.x-self.x) + (i.y-self.y)*(i.y-self.y)
                if   distance < self.vrange*self.vrange :
                    py.draw.line(boid.SURFACE,(0,255,0),(int(self.x),int(self.y)),(int(i.x),int(i.y)),1)
                    avgvx+=i.vx
                    avgvy+=i.vy
                    avgx+=i.x
                    avgy+=i.y
                    count+=1
                    if(distance!=0):
                        diffx=self.x-i.x    
                        diffy = self.y-i.y
                        diffx/=(distance)
                        diffy/=(distance)
                        repx+=diffx
                        repy+=diffy
                        repc+=1

        if count>0:
            #alignement
            avgvx=avgvx/count
            avgvy=avgvy/count
            nn = n(avgvx,avgvy)
            if nn>0:
                avgvx/=nn
                avgvy/=nn
                avgvx*=self.maxspeed
                avgvy*=self.maxspeed
            avgvx-=self.vx
            avgvy-=self.vy

            #cohesion
            avgy=avgy/count
            avgx=avgx/count
            avgx-=self.x
            avgy-=self.y
            nn = n(avgx,avgy)
            if nn> 0:
                avgx/=nn
                avgy/=nn
                avgx*=self.maxspeed
                avgy*=self.maxspeed
            avgx-=self.vx
            avgy-=self.vy
            nn = n(avgx,avgy)
            if nn> self.maxforce:
                avgx/=nn
                avgy/=nn
                avgx*=self.maxforce
                avgy*=self.maxforce
                
        #separation
        if repc>0:
            repx/=repc
            repy/=repc
            nn=n(repx,repy)
            if nn>0:
                repx/=nn
                repy/=nn
                repx*=self.maxspeed
                repy*=self.maxspeed
            repx-=self.vx
            repy-=self.vy
            nn=n(repx,repy)
            if nn>self.maxforce:
                repx/=nn
                repy/=nn
                repx*=self.maxforce
                repy*=self.maxforce

         #alignement
        self.ax+=avgvx
        self.ay+=avgvy
        #grouping
        self.ax+=avgx
        self.ay+=avgy
        #repulsion
        self.ax+=repx
        self.ay+=repy
        txt1 = font.render("ali "+str(int(avgvx*10))+" " + str(int(avgvy*10)), True, py.Color('white'))
        txt2 = font.render("grou "+str(int(avgx*10))+" "+str(int(avgy*10)),True,py.Color('white'))
        txt3 = font.render("rep "+str(int(repx*10))+" "+str(int(repy*10)),True,py.Color('white'))
        boid.SURFACE.blit(txt1,(int(self.x),int(self.y)))
        boid.SURFACE.blit(txt2,(int(self.x),int(self.y+25)))
        boid.SURFACE.blit(txt3,(int(self.x),int(self.y+45)))


    def localise(self):
        xx= int(self.x/splintercell.WIDTH)
        yy= int(self.y/splintercell.HEIGHT)
        if xx>0 and xx<(int(splintercell.SWIDTH / splintercell.WIDTH)) and yy>0 and yy<(int(splintercell.SHEIGHT/splintercell.HEIGHT)):
            # print("                                                  ")
            # for i in splintercell.TABLE:
            #     print(i)
            # print("                                                  ")
            #print(xx , yy)
            splintercell.TABLE[yy][xx].append(self)
    
    def findclose(self):
        xx= int(self.x/splintercell.WIDTH)
        yy= int(self.y/splintercell.HEIGHT)
        py.draw.rect(boid.SURFACE,(255,0,0),py.Rect(xx*splintercell.WIDTH,yy*splintercell.HEIGHT,splintercell.WIDTH,splintercell.HEIGHT),1)
        py.draw.line(boid.SURFACE,(200,0,0),(int(self.x),int(self.y)),(int(xx*splintercell.WIDTH),int(yy*splintercell.HEIGHT)),1)
        arr=[]
        for i in range(-1,2):
            for j in range(-1,2):
                arr.append(splintercell.get(xx+i,yy+j))
        for i in arr:
            self.align(i)

    def draw(self):
        if self.shape == "circle":
            py.draw.circle(boid.SURFACE,self.color,(int(self.x),int(self.y)),int(self.radius))
        if self.shape == "line":
            nn=n(self.vx,self.vy)/4
            if nn>0:
                py.draw.line(boid.SURFACE,self.color,(int(self.x),int(self.y)),(int(self.x+self.vx/nn),int(self.y+self.vy/nn)))
            else:
                py.draw.circle(boid.SURFACE,self.color,(int(self.x),int(self.y)),1)
    @staticmethod
    def generaterandompos(quantity):
        (w, h) = boid.SURFACE.get_size()
        for _ in range(quantity):
            boid.ARRAY.append(boid(np.random.random_integers(0,w),np.random.random_integers(0,h)))
    @staticmethod 
    def drawall():
        splintercell.TABLE=[]
        splintercell.init()
        for i in boid.ARRAY:
            i.localise()
        for i in boid.ARRAY:
            #i.align(boid.ARRAY)
            i.findclose()
            i.apply()
            i.draw()