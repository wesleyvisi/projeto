# -*- coding: utf-8 -*-
import numpy as np
import cv2
import time
import sys
from objeto import Objeto
from imagens import Imagens
from settings import Settings
import threading 




class Camera(object):
    
    
    def __init__(self, id, nome, camera, angulo, proporcao,areasSeguras, saidas, status):
        self.id = id
        self.nome = nome
        self.camera = camera
        self.angulo = angulo
        self.proporcao = proporcao
        self.areasSeguras = areasSeguras
        self.saidas = saidas
        self.status = status
        
        self.settings = Settings()
                
        self.indiceStatus = self.status.novoComodo(self.nome,self.settings.COMODO_VAZIO,0)
        
        self.tempoPessoa = self.settings.tempoParaAlerta
        self.tempoObjeto = self.settings.tempoParaMoverObjeto
        
        
        
        
        print("carregando... ")
        self.imagens = Imagens(self.id,self.camera, self.angulo, self.proporcao)
        
        
        
        
        self.lista = []
    
        
        self.showThr = threading.Thread(target=self.show,args=())
        self.showThr.start()
        
        self.continua = True
        
        self.runThr = threading.Thread(target=self.run,args=())
        self.runThr.start()
        
        
        
    def run(self):
        
        
        self.imagens.start()
        self.ajustaAreas()
        
        
        
        while self.continua:
            
            if(self.imagens.pegandoBackground == False):
                
                self.imagens.readFrame()
                
                contours = self.imagens.pegarContornos()
                
                
                for contour in contours:
                    
                    (x, y, w, h) = cv2.boundingRect(contour)
                    
                    
                    
                    salva = True
                    for nitem in range(0, len(self.lista)):
                        
                        if(not salva):
                            break
                            
                            
                        item = self.lista[nitem]
                        
                        area = item.verificaArea(x, y, w, h)
                        
        
                        if((cv2.contourArea(contour) < self.settings.areaMinimaParaBg) & (w < (h * 4)) & (w > (h * 0.20)) & (not area)):
                            salva = False
                            self.imagens.atualizaBackground(x,y,w,h)
                            
                            break
                        
                        if(cv2.contourArea(contour) < self.settings.areaMinimaParaBg):
                            break
                        
                        
                        self.imagens.atualizaUltimoMovimento()
                        
                        if(area):
                            
                            salva = False
            
            
                            if(item.ultimoFrame == self.imagens.numFrame):
                                if x > item.x:
                                    x = item.x
                                    
                                if y > item.y:
                                    y = item.y
                                    
                                if x + w < item.x + item.w:
                                    w = (item.x + item.w) - x
                                    
                                if y + h < item.y + item.h:
                                    h = (item.y + item.h) - y
                            else:
                                item.areaAnterior = [item.x,item.y,item.w,item.h]
                                    
                                
                            item.x = x
                            item.y = y
                            item.w = w
                            item.h = h
                            item.ultimoFrame = self.imagens.numFrame
                            
                            
                            break
                        
                    
                        
                    
                    #se o quadrado não estiver na lista salva ele
                    if(salva & (cv2.contourArea(contour) > self.settings.areaMinimaParaLista)):
                        self.lista.append(Objeto(x, y, w, h,[x, y, w, h],time.time(),self.imagens.numFrame,self.imagens))
                                
                        
                
                
                
                    
                
                #a cada 5 frames verifica por quadrados duplicados
                if(self.imagens.numFrame % self.settings.framesVerificaQadrados == 0):
                    
                    self.verificaQuadradoDuplicadoOuGrande()
                    
                    
                    
                self.atualizaTime()      
                     
                        
                    
                #Marca quadrados na imagem
                
                for nitem in range(0, len(self.lista)):
                    
                    item = self.lista[nitem]
                    
                    x = item.x
                    y = item.y
                    w = item.w
                    h = item.h
                    
                    
                        
                    
                    #cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
                    #cv2.putText(imagens.frame, "{}".format(str(int(time.time() - item.ultimoMovimento))), (x, y+110), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                    if((item.pessoa()) & (item.tempoParado() > self.tempoPessoa)):
                        cv2.putText(self.imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 2)
                        cv2.putText(self.imagens.frame, "{}".format("SOS"), (x, y+120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 10)
                        cv2.rectangle(self.imagens.frame, (x, y), (x + w, y + h), (0,0,255), 3)
                        
                        self.status.setStatusComodo(self.indiceStatus,self.settings.ALERTA_RISCO,self.imagens.numFrame)
                        
                        
                    elif(item.pessoa() ):
                        cv2.putText(self.imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
                        cv2.putText(self.imagens.frame, "{}".format(str(int(item.tempoParado()))), (x, y+120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,255), 3)
                        cv2.rectangle(self.imagens.frame, (x, y), (x + w, y + h), (0,255,0), 3)
                        
                        if((self.status.getFrameComodo(self.indiceStatus) < self.imagens.numFrame) | (self.status.getStatusComodo(self.indiceStatus) == self.settings.OBJETO_NO_COMODO)):
                            self.status.setStatusComodo(self.indiceStatus,self.settings.PESSOA_NO_COMODO,self.imagens.numFrame)
                        
                        
                    elif(item.tempoParado() > self.tempoObjeto):
                        self.imagens.atualizaBackground(item.x,item.y,item.w,item.h)  
                        
                    else:
                        cv2.putText(self.imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50,255,255), 2)
                        cv2.rectangle(self.imagens.frame, (x, y), (x + w, y + h), (50,255,255), 3)
                        
                        if(self.status.getFrameComodo(self.indiceStatus) < self.imagens.numFrame):
                            self.status.setStatusComodo(self.indiceStatus,self.settings.OBJETO_NO_COMODO,self.imagens.numFrame)
                        
                    
                
                
                    
                self.imagens.atualizaFrameShow()
            
            
                
                
                if(self.imagens.numFrame % self.settings.framesVerificaQadrados == 0):
                    self.verificaQuadradosVazios()
                
                
                
            
            
            
            
        video_capture.release()
        cv2.destroyAllWindows()
    
    
    
    
    def ajustaAreas(self):
        seguras = self.areasSeguras
        saidas = self.saidas
        
        self.areasSeguras = []
        self.saidas = []
        
        
        for area in seguras:
            self.areasSeguras.append(
                    [
                        int(self.imagens.larguraImagem * (float(area[0]) / 100)),
                        int(self.imagens.alturaImagem * (float(area[1]) / 100)),
                        int(self.imagens.larguraImagem * (float(area[2]) / 100)),
                        int(self.imagens.alturaImagem * (float(area[3]) / 100))
                    ]
                )
        
        for area in saidas:
            self.saidas.append(
                    [
                        area[0],
                        [
                            int(self.imagens.larguraImagem * (float(area[1][0]) / 100)),
                            int(self.imagens.alturaImagem * (float(area[1][1]) / 100)),
                            int(self.imagens.larguraImagem * (float(area[1][2]) / 100)),
                            int(self.imagens.alturaImagem * (float(area[1][3]) / 100))
                        ]
                        
                    ]
                )
            
            
            
            
            
        
        
        
    def show(self):
        
        time.sleep(1)
        while True:
            if(not (self.imagens is None)):
                if(not self.imagens.pegandoBackground):
                    time.sleep(0.2)
                    
                    for area in self.saidas:
                        area = area[1]
                        cv2.rectangle(self.imagens.frameShow, (area[0], area[1]), (area[0] + area[2], area[1] + area[3]), (0,0,0), 1)
                    for area in self.areasSeguras:
                        cv2.rectangle(self.imagens.frameShow, (area[0], area[1]), (area[0] + area[2], area[1] + area[3]), (200,0,0), 1)
                    
                    
                    #cv2.imshow("bin - "+self.camera,self.imagens.bin)
                    #cv2.imshow("bg - "+str(self.camera),self.imagens.bg)
                    cv2.imshow("Frame - "+str(self.camera),self.imagens.frameShow)
                    #cv2.imshow("Primary - "+self.camera,self.imagens.primarybg)
                    
                    waitKey = cv2.waitKey(1) 
                    if waitKey & 0xFF == ord('q'):  
                        cv2.destroyAllWindows()
                        self.imagens.stopImagens()
                        for item in self.lista:
                            item.stopObjeto()
                        self.continua = False
                        break
                    
                    if waitKey & 0xFF == ord('n'):     
                        cv2.destroyAllWindows()
                        self.imagens.pegarBg()
            
    
    
    
    
    def verificaQuadradoDuplicadoOuGrande(self):
        num1 = 0;
        num2 = 0;
        while num1 < len(self.lista):
                        
            if(self.lista[num1].w * self.lista[num1].h >= ((self.imagens.larguraImagem * self.imagens.alturaImagem) * self.settings.proporcaoQuadradoTelaParaBg)):
                self.imagens.pegarBg()
                            
                            
            num2 = num1 + 1
                        
            while num2 < len(self.lista):
                if ((self.lista[num1].x == self.lista[num2].x) &
                        (self.lista[num1].y == self.lista[num2].y) & (self.lista[num1].w == self.lista[num2].w) &
                        (self.lista[num1].h == self.lista[num2].h)):
                    self.lista[num2].stopObjeto()
                    self.lista.pop(num2)
                else:
                    num2 = num2 + 1
            num1 = num1 + 1
    
    
    
    def atualizaTime(self):
        for nitem in range(0, len(self.lista)):
            item = self.lista[nitem]
                    
            if((item.x <= (item.areaAnterior[0] - self.settings.variacaoMovimento)) |
                (item.x >= (item.areaAnterior[0] + self.settings.variacaoMovimento)) |
                (item.y <= (item.areaAnterior[1] - self.settings.variacaoMovimento)) |
                (item.y >= (item.areaAnterior[1] + self.settings.variacaoMovimento)) |
                (item.w <= (item.areaAnterior[2] - self.settings.variacaoMovimento)) |
                (item.w >= (item.areaAnterior[2] + self.settings.variacaoMovimento)) |
                (item.h <= (item.areaAnterior[3] - self.settings.variacaoMovimento)) |
                (item.h >= (item.areaAnterior[3] + self.settings.variacaoMovimento)) ):
                        
                item.ultimoMovimento = time.time() 
            
            for area in self.areasSeguras:
                if(item.pessoa() &
                    (item.x >= (area[0] - self.settings.variacaoMovimento)) &
                    (item.y >= (area[1] - self.settings.variacaoMovimento)) &
                    (item.w <= (area[2] + self.settings.variacaoMovimento)) &
                    (item.h <= (area[3] + self.settings.variacaoMovimento)) ):
                            
                    item.ultimoMovimento = time.time() 
    
    
    
    
    def verificaQuadradosVazios(self):
        nitem = 0
        while(nitem < len(self.lista)):
            local = 0
            if(self.lista[nitem].ultimoFrame < self.imagens.numFrame - 2):
                for area in self.saidas:
#                     print((self.lista[nitem]))
#                     print(area[1])
                    
                    if(self.lista[nitem].pessoa() &
                        (self.lista[nitem].x >= (area[1][0] - self.settings.variacaoMovimento)) &
                        (self.lista[nitem].y >= (area[1][1] - self.settings.variacaoMovimento)) &
                        (self.lista[nitem].w <= (area[1][2] + self.settings.variacaoMovimento)) &
                        (self.lista[nitem].h <= (area[1][3] + self.settings.variacaoMovimento)) ):
                        if(area[0] == self.settings.SAIDA_CASA):
                            self.status.setStatusComodo(self.indiceStatus,self.settings.SAIU_DA_CASA,self.imagens.numFrame)
                        elif(area[0] == self.settings.SAIDA_COMODO):
                            self.status.setStatusComodo(self.indiceStatus,self.settings.COMODO_VAZIO,self.imagens.numFrame)
                        elif(area[0] == self.settings.SAIDA_BANHEIRO):
                            self.status.setStatusComodo(self.indiceStatus,self.settings.PODE_ESTAR_NO_BANHEIRO,self.imagens.numFrame)
                    
                    
                self.lista[nitem].stopObjeto()
                self.lista.pop(nitem)
            else:
                nitem = nitem + 1
                
        if((len(self.lista) == 0) & 
            (self.status.getStatusComodo(self.indiceStatus) != self.settings.SAIU_DA_CASA) & 
            (self.status.getStatusComodo(self.indiceStatus) != self.settings.COMODO_VAZIO) & 
            (self.status.getStatusComodo(self.indiceStatus) != self.settings.PODE_ESTAR_NO_BANHEIRO)
            ):
            
            self.status.setStatusComodo(self.indiceStatus,self.settings.COMODO_VAZIO,self.imagens.numFrame)
    
    
    def setTempo(self,tempoPessoa,tempoObjeto):
        self.tempoPessoa = tempoPessoa
        self.tempoObjeto = tempoObjeto
    
    
    
    
    
    
    
