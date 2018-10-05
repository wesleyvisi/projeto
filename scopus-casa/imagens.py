from _ast import Num
import numpy as np
import sys
import threading 
import time
import cv2


class Imagens(object):
    
    def __init__(camera, rotacao):
        
        self.stop = False
        
        self.rotacao
        
        self.video_capture = cv2.VideoCapture(camera)
        ret, preFrame = self.video_capture.read()
        
        self.frame = gira(preFrame)
        
        self.alturaImagem, self.larguraImagem = self.frame.shape[:2]
        time.sleep(1)
        
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        self.primarybg = self.gray.copy()
        
        self.bg =  self.gray.copy()
        
        self.pegarBackground()
        
        
        
        
        
        limpabg = threading.Thread(target=limpaBg,args=())
        limpabg.start()
        
        
        
    
    def stopImagens(self):
        self.video_capture.release()
        self.stop = True
    
        
        
    def limpaBg(self):
        while not self.stop:
            time.sleep(20)
            print("Limpando Bg")
                
            dif = cv2.absdiff(self.primarybg, self.gray)
            dif = cv2.threshold(dif, 10, 255, cv2.THRESH_BINARY)[1]
                    
                    
            for y in range(0,primarybg.shape[0]):
                for x in range(0,primarybg.shape[1]):
                    if(dif[y,x] == 0):
                        bg[y,x] = gray[y,x] 
        




        
    def pegarBackground(self):
        
        contours = [1,2]
        
        ret, preFrame = self.video_capture.read()
        
        frame = gira(preFrame)
        
        self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
        
        while(len(contours) > 0):
            ret, preFrame = self.video_capture.read()
            
            frame = gira(preFrame)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(primarybg, gray)
            dilate = cv2.dilate(dif, None, iterations=5)
            bin = cv2.threshold(dilate, 18, 255, cv2.THRESH_BINARY)[1]
            _, contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
                
        self.bg = self.primarybg.copy()

    
    
    
    def atualizaBackground(self,x,y,w,h):
        for cy in range(y,y+h):
            for cx in range(x,x+w):
                self.bg[cy,cx] = self.gray[cy,cx]
        

    
    
    def gira(self,frame):
        
        if(rotacao == 90):
            altura, largura = frame.shape[:2]
            frame = cv2.resize(frame,(largura,largura))
            ponto = (largura / 2, largura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 90, 1.0)
            rotacionado = cv2.warpAffine(frame, rotacao, (largura, largura))
            return cv2.resize(rotacionado,(int(altura/1),int(largura/1)))
        
        if(rotacao == 180):
            altura, largura = frame.shape[:2]
            ponto = (altura / 2, largura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 180, 1.0)
            return cv2.warpAffine(frame, rotacao, (altura, largura))
        
        if(rotacao == 270):
            altura, largura = frame.shape[:2]
            frame = cv2.resize(frame,(largura,largura))
            ponto = (largura / 2, largura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 270, 1.0)
            rotacionado = cv2.warpAffine(frame, rotacao, (largura, largura))
            return cv2.resize(rotacionado,(int(altura/1),int(largura/1)))
        
        
        
        
        