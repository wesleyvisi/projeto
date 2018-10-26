from _ast import Num
import numpy as np
import sys
import threading 
import time
import cv2
from time import sleep


class Imagens(object):
    
    def __init__(self,camera, rotacao,proporcao):
        
        self.stop = False
        
        self.rotacao = rotacao
        self.proporcao = proporcao
        
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
        
        self.pegandoBackground = False
        
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
            
            if(self.pegandoBackground == False):
                    
                print("Limpando Bg")
                
                gray = self.gray.copy()
                    
                dif = cv2.absdiff(self.primarybg, gray)
                dif = cv2.threshold(dif, 10, 255, cv2.THRESH_BINARY)[1]
                        
                        
                for y in range(0,self.primarybg.shape[0]):
                    for x in range(0,self.primarybg.shape[1]):
                        if(dif[y,x] == 0):
                            self.bg[y,x] = gray[y,x] 
            




        
    def pegarBackground(self):
        
        self.pegandoBackground = True
        
        contours = [1,2]
        
        ret, preFrame = self.video_capture.read()
        
        frame = self.gira(preFrame)
        
        self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cont = 0
        sensibilidade = 5
        while((len(contours) > 0) & (cont < 130)):
            cont = cont+1
            if(cont > 50):
                sensibilidade = 10
            time.sleep(0.1)
            print(cont)
            ret, preFrame = self.video_capture.read()
            
            frame = self.gira(preFrame)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(self.primarybg, gray)
            dilate = cv2.dilate(diff, None, iterations=5)
            bin = cv2.threshold(dilate, sensibilidade, 255, cv2.THRESH_BINARY)[1]
            _, contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                (xx, xy, xw, xh) = cv2.boundingRect(contour)
                cv2.rectangle(self.primarybg, (xx, xy), (xx + xw, xy + xh), (0,0,255), 3)
            
            
            self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                
        if(cont == 130):
            
            img1 = cv2.imread("bg/1.jpg",cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread("bg/2.jpg",cv2.IMREAD_GRAYSCALE)
            
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                
                quadro1 = img1[y:y+h, x:x+w]
                quadro2 = img2[y:y+h, x:x+w]
                
                new = cv2.absdiff(quadro1, quadro2)
    
                new = cv2.threshold(new, 10, 255, cv2.THRESH_BINARY)[1]
                igual = 0
                diferente = 0
                for ty in range(0, new.shape[0]):
                    for tx in range(0, new.shape[1]):
                        if(new[ty,tx] == 0):
                            igual = igual + 1
                        else:
                            diferente = diferente + 1
                            
                if(igual > diferente * 2):
                    print(x , w, y , h)
                    for cy in range(y,y+h):
                        for cx in range(x,x+w):
                            self.primarybg[cy,cx] = img2[cy,cx]
                
                cv2.rectangle(img1, (x, y), (x + w, y + h), (50,200,50), 2)
            
            
            
            
        self.bg = self.primarybg.copy()
        
        self.pegandoBackground = False
            
        
        
        
        
        
        

    
    
    
    def atualizaBackground(self,x,y,w,h):
        for cy in range(y,y+h):
            for cx in range(x,x+w):
                self.bg[cy,cx] = self.gray[cy,cx]
        

    
    
    def gira(self,frame):
        
        altura, largura = frame.shape[:2]
        
        if(self.rotacao == 90):
            frame = cv2.resize(frame,(largura,largura))
            ponto = (largura / 2, largura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 90, 1.0)
            rotacionado = cv2.warpAffine(frame, rotacao, (largura, largura))
            return cv2.resize(rotacionado,(int(altura * self.proporcao),int(largura * self.proporcao)))
        
        if(self.rotacao == 180):
            ponto = (largura / 2, altura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 180, 1.0)
            return cv2.warpAffine(frame, rotacao, (int(largura * self.proporcao), int(altura * self.proporcao)))
        
        if(self.rotacao == 270):
            frame = cv2.resize(frame,(largura,largura))
            ponto = (largura / 2, largura / 2) #ponto no centro da figura
            rotacao = cv2.getRotationMatrix2D(ponto, 270, 1.0)
            rotacionado = cv2.warpAffine(frame, rotacao, (largura, largura))
            return cv2.resize(rotacionado,(int(altura * self.proporcao),int(largura * self.proporcao)))
        
        if(self.proporcao != 1):
            frame = cv2.resize(frame,(int(largura * self.proporcao),int(altura * self.proporcao)))
        return frame
        
        
    def pegarContornos(self):
        new = cv2.absdiff(self.bg, self.gray)
    
        new = cv2.dilate(new, None, iterations=3)
        
        new = cv2.threshold(new, 60, 255, cv2.THRESH_BINARY)[1]
        
        self.bin = cv2.dilate(new, np.ones((9,3), np.uint8), iterations=5)
        
        _, contours, _ = cv2.findContours(new, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    
    
    def atualizaFrameShow(self):
        self.frameShow = self.frame
    
    
    
    
    
    
    
    
    
    