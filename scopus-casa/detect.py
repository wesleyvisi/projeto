# -*- coding: utf-8 -*-

import numpy as np
import cv2
import time
import sys
from objeto import Objeto
from imagens import Imagens
import threading 
import datetime 
from datetime import date





def show(imagens):
    time.sleep(1)
    while True:
        time.sleep(0.2)
        cv2.imshow("bin",imagens.bin)
        cv2.imshow("bg",imagens.bg)
        cv2.imshow("Frame",imagens.frameShow)
        cv2.imshow("primary",imagens.primarybg)
        cv2.waitKey(1)
    





print("carregando... ")
imagens = Imagens("rtsp://192.168.1.109:554/user=admin&password=raspcam&channel=1&stream=0.sdp?",0,0.7)
#imagens = Imagens(0,0,1)
#datetime.datetime.now()







lista = []


show = threading.Thread(target=show,args=(imagens,))
show.start()

while 1:
    
    imagens.readFrame()
    
    contours = imagens.pegarContornos()
    
    
    for contour in contours:
        
        (x, y, w, h) = cv2.boundingRect(contour)
        
        
        
        '''if (((y + h) < (imagens.alturaImagem / 3)) &   (cv2.contourArea(contour) < 35*35) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            imagens.atualizaBackground(x,y,w,h)
            
            continue
        
        if (((y + h) > (imagens.alturaImagem / 3)) & ((y + h) < ((imagens.alturaImagem / 3)) * 2) &   (cv2.contourArea(contour) < ((35*35)*2)) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            imagens.atualizaBackground(x,y,w,h)
            
            continue
        
        if (((y + h) > ((imagens.alturaImagem / 3)) * 2) &   (cv2.contourArea(contour) < ((35*35)*3)) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            imagens.atualizaBackground(x,y,w,h)
            
            continue
        
        
        if cv2.contourArea(contour) < 60*60:
            continue'''
        
        
        
        color = (0, 255, 0)
        
        salva = True
        for nitem in range(0, len(lista)):
            
            if(not salva):
                continue
                
                
            item = lista[nitem]
            
            area = item.verificaArea(x, y, w, h)
            
            if (((((y + h) < (imagens.alturaImagem / 3)) &   (cv2.contourArea(contour) < 35*35) & (w < (h * 4)) & (w > (h * 0.20)) )  |
                (((y + h) > (imagens.alturaImagem / 3)) & ((y + h) < ((imagens.alturaImagem / 3)) * 2) &   (cv2.contourArea(contour) < ((35*35)*2)) & (w < (h * 4)) & (w > (h * 0.20)) )  |
                (((y + h) > ((imagens.alturaImagem / 3)) * 2) &   (cv2.contourArea(contour) < ((35*35)*3)) & (w < (h * 4)) & (w > (h * 0.20)) )
                ) & (not area)):
                salva = False
                imagens.atualizaBackground(x,y,w,h)
                
                continue
            
            
            
            
            if cv2.contourArea(contour) < 70*70:
                salva = False
                continue
                
            
            
            
           
            
            if(area):
                
                salva = False


                if(item.ultimoFrame == imagens.numFrame):
                    if x > item.x:
                        x = item.x
                        
                    if y > item.y:
                        y = item.y
                        
                    if x + w < item.x + item.w:
                        w = (item.x + item.w) - x
                        
                    if y + h < item.y + item.h:
                        h = (item.y + item.h) - y
                        
                    if(w > item.areaAnterior[2] + 30 | h > item.areaAnterior[3] + 30):
                        salva = True
                        continue
                        
                    
                
                
                item.areaAnterior = [item.x,item.y,item.w,item.h]
                item.x = x
                item.y = y
                item.w = w
                item.h = h
                item.ultimoFrame = imagens.numFrame
                
                continue
            
        
            
        
        #se o quadrado não estiver na lista salva ele
        if(salva):
            lista.append(Objeto(x, y, w, h,[x, y, w, h],time.time(),imagens.numFrame,imagens))
                    
            
    
    
    
        
    
    #a cada 5 frames verifica por quadrados duplicados
    if(imagens.numFrame % 5 == 0):
        
        num1 = 0;
        num2 = 0;
        while num1 < len(lista):
            
            if(lista[num1].w * lista[num1].h >= ((imagens.larguraImagem * imagens.alturaImagem) * 0.9)):
                imagens.pegarBackground()
                
                
            num2 = num1 + 1
            
            while num2 < len(lista):
                if ((lista[num1].x == lista[num2].x) & (lista[num1].y == lista[num2].y) & (lista[num1].w == lista[num2].w) & (lista[num1].h == lista[num2].h)):
                    lista[num2].stopObjeto()
                    lista.pop(num2)
                else:
                    num2 = num2 + 1
            num1 = num1 + 1
        
        
        
    for nitem in range(0, len(lista)):
        item = lista[nitem]
        #if((item.x >= (item.areaAnterior[0] - (item.w * 0.02))) & (item.x <= (item.areaAnterior[0] + (item.w * 0.02))) & (item.y >= (item.areaAnterior[1] -(item.h * 0.02))) & (item.y <= (item.areaAnterior[1] + (item.h * 0.02)))   &   (item.w >= (item.areaAnterior[2] - (item.w * 0.02))) & (item.w <= (item.areaAnterior[2] + (item.w * 0.02))) & (item.h >= (item.areaAnterior[3] - (item.h * 0.02))) & (item.h <= (item.areaAnterior[3] + (item.h * 0.02))) ):
        if((item.x <= (item.areaAnterior[0] - 5)) |
            (item.x >= (item.areaAnterior[0] + 5)) |
             (item.y <= (item.areaAnterior[1] - 5)) |
              (item.y >= (item.areaAnterior[1] + 5)) |
               (item.w <= (item.areaAnterior[2] - 5)) |
                (item.w >= (item.areaAnterior[2] + 5)) |
                 (item.h <= (item.areaAnterior[3] - 5)) |
                  (item.h >= (item.areaAnterior[3] + 5)) ):
            item.ultimoMovimento = time.time()        
         
            
        
    #Marca quadrados na imagem
    for nitem in range(0, len(lista)):
        
        item = lista[nitem]
        
        x = item.x
        y = item.y
        w = item.w
        h = item.h
        
        
            
        
        #cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
        #cv2.putText(imagens.frame, "{}".format(str(int(time.time() - item.ultimoMovimento))), (x, y+110), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        if((item.pessoa()) & (item.tempoParado() > 15)):
            cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 2)
            cv2.putText(imagens.frame, "{}".format("SOS"), (x, y+120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 10)
            cv2.rectangle(imagens.frame, (x, y), (x + w, y + h), (0,0,255), 3)
        elif(item.pessoa() ):
            cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
            cv2.putText(imagens.frame, "{}".format(str(int(item.tempoParado()))), (x, y+120), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0), 2)
            cv2.rectangle(imagens.frame, (x, y), (x + w, y + h), (0,255,0), 3)
            
        elif(item.tempoParado() > 15):
            imagens.atualizaBackground(item.x,item.y,item.w,item.h)  
        else:
            cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50,255,255), 2)
            cv2.rectangle(imagens.frame, (x, y), (x + w, y + h), (50,255,255), 3)
        
    
    
        
    imagens.atualizaFrameShow()


    
    
    if(imagens.numFrame % 5 == 0):
        nitem = 0
        while(nitem < len(lista)):
            if(lista[nitem].ultimoFrame < imagens.numFrame - 2):
                lista[nitem].stopObjeto()
                lista.pop(nitem)
            else:
                nitem = nitem + 1
    
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('n'):     
        cv2.destroyAllWindows()
        
        imagens.pegarBackground()
        
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
video_capture.release()
cv2.destroyAllWindows()

