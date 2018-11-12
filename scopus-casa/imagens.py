from _ast import Num
import numpy as np
import sys
import threading 
import time
import cv2
from time import sleep
import os
from settings import Settings


class Imagens(object):
    
    def __init__(self,cameraId,camera, rotacao,proporcao):
        
        self.cameraId = cameraId
        
        self.stop = False
        
        self.rotacao = rotacao
        self.proporcao = proporcao
        
        self.settings = Settings()
        
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
        
        self.ultimoMovimento = time.time()
        
        
        
        
        
        new = cv2.absdiff(self.bg, self.gray)
        new = cv2.dilate(new, None, iterations=2)
        self.bin = cv2.threshold(new, 50, 255, cv2.THRESH_BINARY)[1]
                
        
        
        
        
    
    def start(self):
        self.pegarBg()
        
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
            time.sleep(self.settings.limpaBgTime)
            
            if(self.pegandoBackground == False):
                    
                print("Limpando Bg")
                
                gray = self.gray.copy()
                    
                dif = cv2.absdiff(self.primarybg, gray)
                dif = cv2.threshold(dif, self.settings.limpaBgSensibilidade, 255, cv2.THRESH_BINARY)[1]
                        
                        
                for y in range(0,self.primarybg.shape[0]):
                    for x in range(0,self.primarybg.shape[1]):
                        if(dif[y,x] == 0):
                            self.bg[y,x] = gray[y,x] 
            




        
    def pegarBg(self):
        
        self.pegandoBackground = True
        
        contours = [1,2]
        
        ret, preFrame = self.video_capture.read()
        
        frame = self.gira(preFrame)
        
        self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cont = 0
        sensibilidade = 6
        while((len(contours) > 0) & (cont < self.settings.pegarBgTentativas)):
            cont = cont+1
            if(cont > 50):
                sensibilidade = self.settings.pegarBgSensibilidade
            time.sleep(0.1)
            print(cont)
            ret, preFrame = self.video_capture.read()
            
            frame = self.gira(preFrame)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(self.primarybg, gray)
            dilate = cv2.dilate(diff, None, iterations=5)
            bin = cv2.threshold(dilate, sensibilidade, 255, cv2.THRESH_BINARY)[1]
            _, contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            
            
            self.primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                
                
        
        
        
        if(cont == self.settings.pegarBgTentativas):
            
            bgs = []
            
            for contArq in range(0,10):
                
                 if(os.path.exists('bg/'+str(self.cameraId)+' - '+str(contArq)+'.jpg')):
                    bgs.append(cv2.imread('bg/'+str(self.cameraId)+' - '+str(contArq)+'.jpg',cv2.IMREAD_GRAYSCALE))
                    altura, largura = bgs[len(bgs)-1].shape[:2]
                    print(str(altura)+"-"+str( largura)+" , "+str(self.alturaImagem)+"-"+str( self.larguraImagem))
                    if(altura != self.alturaImagem | largura != self.larguraImagem):
                        bgs[len(bgs)-1] = cv2.resize(bgs[len(bgs)-1],(self.larguraImagem,self.alturaImagem))
                    altura, largura = bgs[len(bgs)-1].shape[:2]
                    print(str(altura)+"-"+str( largura)+" , "+str(self.alturaImagem)+"-"+str( self.larguraImagem))
            
           
            
            
            
            
            semelhante = self.primarybg.copy()
            numSemelhante = 0;
            for img in bgs:
                quadro2 = img
                new = cv2.absdiff(self.primarybg, quadro2)
                    
                igual = np.count_nonzero(new == 0);
                    
                
                                
                if(igual > numSemelhante):
                    numSemelhante = igual
                    semelhante = img
                        
                        
            
            
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                
                
                             
                    
                    
                for cy in range(y,y+h):
                    for cx in range(x,x+w):
                        self.primarybg[cy,cx] = semelhante[cy,cx]
                        
                        
            self.aguardeBgThr = threading.Thread(target=self.aguardeBg,args=())
            self.aguardeBgThr.start()
                
#                 
                
        else:
            
            for contArq in range(0,9):
                if(os.path.exists('bg/'+str(self.cameraId)+' - '+str(8 - contArq)+'.jpg')):
                    
                    os.rename('bg/'+str(self.cameraId)+' - '+str(8 - contArq)+'.jpg', 'bg/'+str(self.cameraId)+' - '+str(9 - contArq)+'.jpg')
            
            cv2.imwrite('bg/'+str(self.cameraId)+' - 0.jpg',self.primarybg)
            
            
            
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
        
        new = cv2.threshold(new, self.settings.pegarContornosSensibilidade, 255, cv2.THRESH_BINARY)[1]
        
        self.bin = cv2.dilate(new, np.ones((9,3), np.uint8), iterations=5)
        
        _, contours, _ = cv2.findContours(new, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
        
        return contours
    
    
    
    
    def atualizaUltimoMovimento(self):
        self.ultimoMovimento = time.time()
    
    
    
    def atualizaFrameShow(self):
        self.frameShow = self.frame
    
    
    
    
    
    def aguardeBg(self):
        time.sleep(10) 
        while(self.ultimoMovimento > (time.time() - self.settings.aguardeBgTime)):
            
            time.sleep(1)
            
            
        self.pegarBg()
    
    
    
    
    
    
    
    
    