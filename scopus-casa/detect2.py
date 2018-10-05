# -*- coding: utf-8 -*-

import numpy as np
import cv2
import time
import sys
from objeto import Objeto
from imagens import Imagens
import threading 





def show(imagens):
    time.sleep(1)
    while True:
        time.sleep(0.2)
        #cv2.imshow("NEW",new)
        cv2.imshow("Frame",imagens.frameShow)
        cv2.imshow("bg",imagens.bg)
    





print("carregando... ")
imagens = Imagens("rtsp://10.42.0.95:554/user=admin&password=raspcam&channel=1&stream=0.sdp?",90)






lista = []


show = threading.Thread(target=show,args=(imagens,))
show.start()

while 1:
    
    imagens.readFrame()
    
    contours = imagens.pegarContornos()
    
    
    for contour in contours:
        
        (x, y, w, h) = cv2.boundingRect(contour)
        
        
        
        if (((y + h) < (imagens.alturaImagem / 3)) &   (cv2.contourArea(contour) < 35*35) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            imagens.atualizaBackground(x,y,w,h)
            
            continue
        
        if (((y + h) > (imagens.alturaImagem / 3)) & ((y + h) < ((imagens.alturaImagem / 3)) * 2) &   (cv2.contourArea(contour) < ((35*35)*2)) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            imagens.atualizaBackground(x,y,w,h)
            
            continue
        
        if (((y + h) > ((imagens.alturaImagem / 3)) * 2) &   (cv2.contourArea(contour) < ((35*35)*3)) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            imagens.atualizaBackground(x,y,w,h)
            
            continue
        
        
        if cv2.contourArea(contour) < 60*60:
            continue
        
        
        
        color = (0, 255, 0)
        
        salva = True
        for nitem in range(0, len(lista)):
            
            item = lista[nitem]
            
           
            
            if(item.verificaArea(x, y, w, h)):
                
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
            lista.append(Objeto(x, y, w, h,[x, y, w, h],time.time(),imagens.numFrame,imagens.gray))
                    
            
    
    
    
        
    
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
        if((item.x >= (item.areaAnterior[0] - 2)) & (item.x <= (item.areaAnterior[0] + 2)) & (item.y >= (item.areaAnterior[1] - 2)) & (item.y <= (item.areaAnterior[1] + 2))   &   (item.w >= (item.areaAnterior[2] - 2)) & (item.w <= (item.areaAnterior[2] + 2)) & (item.h >= (item.areaAnterior[3] - 2)) & (item.h <= (item.areaAnterior[3] + 2)) ):
            
            if((item.tempoParado() > 5) & (item.pessoa())):
                cv2.putText(imagens.frame, "{}".format("SOS"), (x, y+250), cv2.FONT_HERSHEY_SIMPLEX, 3, color, 3)
               
            if((item.tempoParado() > 10) & (item.pessoa() == False)):
                imagens.atualizaBackground(item.x,item.y,item.w,item.h)         
                            
        else:
            item.ultimoMovimento = time.time()
        
    #Marca quadrados na imagem
    for nitem in range(0, len(lista)):
        
        item = lista[nitem]
        
        x = item.x
        y = item.y
        w = item.w
        h = item.h
        
        
            
        
        cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
        cv2.putText(imagens.frame, "{}".format(str(item.ultimoMovimento)), (x, y+180), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        if(item.pessoa()):
            cv2.rectangle(imagens.frame, (x, y), (x + w, y + h), (0,0,255), 2)
        else:
            cv2.rectangle(imagens.frame, (x, y), (x + w, y + h), (50,200,50), 2)
        
    
    
        
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

