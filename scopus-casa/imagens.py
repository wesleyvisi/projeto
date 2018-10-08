from _ast import Num
import numpy as np
import sys
import threading 
import time
import cv2
from time import sleep


class Imagens(object):
    
    def __init__(self,camera, rotacao):
        
        self.stop = False
        
        self.rotacao = rotacao
        
        self.numFrame = 0
        
        self.video_capture = cv2.VideoCapture(camera)
        ret, preFrame = self.video_capture.read()
        
        self.frame = self.gira(preFrame)
        
        self.alturaImagem, self.larguraImagem = self.frame.shape[:2]
        time.sleep(1)
        
        self.frameShow = self.frame.copy()
        self.bin = self.frame.copy()
        
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        self.primarybg = self.gray.copy()
        
        self.bg =  self.gray.copy()
        
        self.pegarBackground()
        
        
        
        
        new = cv2.absdiff(self.bg, self.gray)
        new = cv2.dilate(new, None, iterations=2)
        self.bin = cv2.threshold(new, 50, 255, cv2.THRESH_BINARY)[1]
                
        
        self.limpabg = threading.Thread(target=self.limpaBg,args=())
        self.limpabg.start()
        
        
        
    
    def stopImagens(self):
        self.video_capture.release()
        self.stop = True
    
    
    def readFrame(self):
        ret, preFrame = self.video_capture.read()
        
        self.frame = self.gira(preFrame)
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        self.numFrame = self.numFrame + 1
    
    
        
        
    def limpaBg(self):
        while not self.stop:
            time.sleep(10)
            print("Limpando Bg")
                
            dif = cv2.absdiff(self.primarybg, self.gray)
            dif = cv2.threshold(dif, 10, 255, cv2.THRESH_BINARY)[1]
                    
                    
            for y in range(0,self.primarybg.shape[0]):
                for x in range(0,self.primarybg.shape[1]):
                    if(dif[y,x] == 0):
                        self.bg[y,x] = self.gray[y,x] 
        




        
    def pegarBackground(self):
        
        
        
        contours = [1,2]
        
        ret, preFrame = self.video_capture.read()
        
        frame = self.gira(preFrame)
        
        self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        while(len(contours) > 0):
            ret, preFrame = self.video_capture.read()
            
            frame = self.gira(preFrame)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(self.primarybg, gray)
            dilate = cv2.dilate(diff, None, iterations=5)
            bin = cv2.threshold(dilate, 18, 255, cv2.THRESH_BINARY)[1]
            _, contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
        self.bg = self.primarybg.copy()
        
        '''
        
        contours = [1,2]
        
        ret, preFrame = self.video_capture.read()
        
        frame = self.gira(preFrame)
        
        #self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #time.sleep(0.4)
        
        
        
        
        
        ret, preFrame = self.video_capture.read()
        frame = self.gira(preFrame)
        temp5 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        
        
        
        while(len(contours) > 0):

            #cv2.imshow("Primary",self.primarybg)
            for i in range(0, 3):
                ret, temp1 = self.video_capture.read()
                
            cv2.imshow("temp1",temp1)
            


            for i in range(0, 3):
                ret, temp2 = self.video_capture.read()

            cv2.imshow("temp2",temp2)
            
            
            
            for i in range(0, 3):
                ret, temp3 = self.video_capture.read()
            
            cv2.imshow("temp3",temp3)
            
            
            for i in range(0, 3):
                ret, temp4 = self.video_capture.read()
            
            cv2.imshow("temp4",temp4)
            
            cv2.imshow("temp5",temp5)
            
            
            
            
            
            
            
            
            
            
            
            ret, preFrame = self.video_capture.read()
            frame = self.gira(preFrame)
            temp5 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break'''
        
        
        
        
        
        

    
    
    
    def atualizaBackground(self,x,y,w,h):
        for cy in range(y,y+h):
            for cx in range(x,x+w):
                self.bg[cy,cx] = self.gray[cy,cx]
        

    
    
    def gira(self,frame):
        
        if(self.rotacao == 90):
            altura, largura = frame.shape[:2]
            frame = cv2.resize(frame,(largura,largura))
            ponto = (largura / 2, largura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 90, 1.0)
            rotacionado = cv2.warpAffine(frame, rotacao, (largura, largura))
            return cv2.resize(rotacionado,(int(altura/1),int(largura/1)))
        
        if(self.rotacao == 180):
            altura, largura = frame.shape[:2]
            ponto = (largura / 2, altura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 180, 1.0)
            return cv2.warpAffine(frame, rotacao, (largura, altura))
        
        if(self.rotacao == 270):
            altura, largura = frame.shape[:2]
            frame = cv2.resize(frame,(largura,largura))
            ponto = (largura / 2, largura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 270, 1.0)
            rotacionado = cv2.warpAffine(frame, rotacao, (largura, largura))
            return cv2.resize(rotacionado,(int(altura/1),int(largura/1)))
        
        return frame
        
        
    def pegarContornos(self):
        new = cv2.absdiff(self.bg, self.gray)
    
        new = cv2.dilate(new, None, iterations=3)
        
        new = cv2.threshold(new, 50, 255, cv2.THRESH_BINARY)[1]
        
        self.bin = cv2.dilate(new, np.ones((9,3), np.uint8), iterations=7)
        
        _, contours, _ = cv2.findContours(new, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    
    
    def atualizaFrameShow(self):
        self.frameShow = self.frame