
import numpy as np
import sys
import time
import threading 
import cv2
from imagens import Imagens
from settings import Settings


class Objeto(object):
    
    indice = 0
    
    def __init__(self, x, y, w, h, areaAnterior, tempo,ultimoFrame,imagens):
        Objeto.indice = Objeto.indice + 1
        self.num = Objeto.indice
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.areaAnterior = areaAnterior
        self.ultimoMovimento = tempo
        self.deteccoes = []
        self.ultimoFrame = ultimoFrame
        self.stop = False
        
        self.settings = Settings()
        
        cascPathUpperBody = "haarcascade/haarcascade_upperbody.xml"
        cascPathFullBody = "haarcascade/haarcascade_fullbody.xml"
        cascPathFrontalFace = "haarcascade/haarcascade_frontalface_default.xml"
        upperbodyCascade = cv2.CascadeClassifier(cascPathUpperBody)
        fullbodyCascade = cv2.CascadeClassifier(cascPathFullBody)
        frontalFaceCascade = cv2.CascadeClassifier(cascPathFrontalFace)
        
                
        self.thr = threading.Thread(target=(self.detecta),args=(imagens,frontalFaceCascade,upperbodyCascade,fullbodyCascade))
        self.thr.start()
        
        
    
    def stopObjeto(self):
        self.stop = True
    
    
    
        
    def tempoParado(self):
        return time.time() - self.ultimoMovimento
    
    
    def deteccoesAdd(self, r):
        self.deteccoes.append(r)
        if(len(self.deteccoes) > self.settings.objetoDeteccoes):
            self.deteccoes.pop(0)
    
    
    def pessoa(self):
       
        
        if(self.deteccoes.count(True) > (len(self.deteccoes) / self.settings.objetoMinDeteccoes)):
            return True
        else: 
            return False
            
            
        
    
    
    
    
        
    def detecta(self,imagens,frontalFaceCascade,upperbodyCascade,fullbodyCascade):
        while not self.stop:
            
            
            quadro = imagens.gray[self.y:self.y+self.h, self.x:self.x+self.w]
            
            
            time.sleep(0.3)
            
            frontalFaces = frontalFaceCascade.detectMultiScale(quadro, scaleFactor=1.2, minNeighbors=1)
                
            if(len(frontalFaces) > 0):
                self.deteccoesAdd(True)
            else:
                upperbodys = upperbodyCascade.detectMultiScale(quadro, scaleFactor=1.2, minNeighbors=1)
                if(len(upperbodys) > 0):
                    self.deteccoesAdd(True)
                else:
                    fullbodys = fullbodyCascade.detectMultiScale(quadro, scaleFactor=1.2, minNeighbors=1)
                    if(len(fullbodys) > 0):
                        self.deteccoesAdd(True)
                    else:
                        self.deteccoesAdd(False)
                    
                    
                
    
    
    
    
    
    def verificaArea(self,x2,y2,w2,h2):
        
        x1 = self.areaAnterior[0]
        y1 = self.areaAnterior[1]
        w1 = self.areaAnterior[2]
        h1 = self.areaAnterior[3]
        
        
        
        x = -1
        y = -1
        w = -1
        h = -1
            
        if((x1 > x2) & ((x2 + w2) > x1) ):
            if((y1 > y2) & ((y2 + h2) > y1) ):
                
                w = x2 + w2 - x1
                if(w1 < w):
                    w = w1
                x = x1
                
                h = y2 + h2 - y1
                if(h1  < h):
                    h = h1
                    
                y = y1
                
            elif((y1 <= y2) & (y2 <= (y1 + h1 )) ):
                
                w = x2 + w2 - x1
                if(w1 < w):
                    w = w1
                    
                x = x1
                
                h = y1 + h1 - y2
                if(h2  < h):
                    h = h2
                    
                y = y2
              
                
        elif((x1 <= x2) & (x2 <= (x1 + w1 )) ):
            if((y1 > y2) & ((y2 + h2) > y1) ):
                
                w = x1 + w1 - x2
                if(w2 < w):
                    w = w2
                    
                x = x2
                
                h = y2 + h2 - y1
                if(h1  < h):
                    h = h1
                    
                y = y1
                    
              
            elif((y1 <= y2) & (y2 <= (y1 + h1 )) ):
                
                w = x1 + w1 - x2
                if(w2 < w):
                    w = w2
                    
                x = x2
                
                h = y1 + h1 - y2
                if(h2  < h):
                    h = h2
                    
                y = y2
                    
        
        if(w == -1 & h == -1):
            return False
        
        A1 = w1 * h1
        A2 = w2 * h2
        A = w * h
        
        if((A > (A1 * self.settings.objetoProporcaoArea)) | (A > (A2 * self.settings.objetoProporcaoArea))):
            return True
        
        else:
            return False
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        