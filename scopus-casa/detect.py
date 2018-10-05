# -*- coding: utf-8 -*-

import numpy as np
import cv2
import time
import sys
from objeto import Objeto
import threading 




def pegarBackground(capcapture):
        
    contours = [1,2]

    ret, preFrame = video_capture.read()
    frame = gira(preFrame)
    primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

    while(len(contours) > 0):
        ret, preFrame = video_capture.read()
        frame = gira(preFrame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new = cv2.absdiff(primarybg, gray)
        new = cv2.dilate(new, None, iterations=5)
        new = cv2.threshold(new, 18, 255, cv2.THRESH_BINARY)[1]
        _, contours, _ = cv2.findContours(new, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        primarybg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
        
    return frame




def atualizaBackground(x,y,w,h,bg,gray):
    for cy in range(y,y+h):
        for cx in range(x,x+w):
            bg[cy,cx] = gray[cy,cx]
    return bg



def gira(frame):
    altura, largura = frame.shape[:2]
    frame = cv2.resize(frame,(largura,largura))
    ponto = (largura / 2, largura / 2) #ponto no centro da figura
    rotacao = cv2.getRotationMatrix2D(ponto, 90, 1.0)
    rotacionado = cv2.warpAffine(frame, rotacao, (largura, largura))
    return cv2.resize(rotacionado,(int(altura/1),int(largura/1)))



              
def show():
    time.sleep(1)
    while True:
        time.sleep(0.2)
        #cv2.imshow("NEW",new)
        cv2.imshow("Frame",frameShow)
        cv2.imshow("bg",bg)
    


def limpaBg():
    while True:
        time.sleep(20)
        print("Limpando Bg")
        
        
        
        dif = cv2.absdiff(primarybg, gray)
        dif = cv2.threshold(dif, 10, 255, cv2.THRESH_BINARY)[1]
            
            
        for y in range(0,primarybg.shape[0]):
            for x in range(0,primarybg.shape[1]):
                if(dif[y,x] == 0):
                    bg[y,x] = gray[y,x] 





print("carregando... ")
video_capture = cv2.VideoCapture("rtsp://10.42.0.95:554/user=admin&password=raspcam&channel=1&stream=0.sdp?")
#video_capture = cv2.VideoCapture(0)

#video_capture.set(5, 1)



ret, preFrame = video_capture.read()
frame = gira(preFrame)
time.sleep(1)
alturaJanela, larguraJanela = frame.shape[:2]

gray = cv2.cvtColor(pegarBackground(video_capture), cv2.COLOR_BGR2GRAY)

primarybg = gray.copy()

bg = primarybg.copy();

limpabg = threading.Thread(target=limpaBg,args=())
limpabg.start()


numFrame = 0

lista = []


new = gray.copy()
frameShow = frame.copy()
show = threading.Thread(target=show,args=())
show.start()

while 1:
    ret, preFrame = video_capture.read()
    frame = gira(preFrame)
    numFrame = numFrame +1
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    new = cv2.absdiff(bg, gray)
    
    new = cv2.dilate(new, None, iterations=2)
    
    new = cv2.threshold(new, 50, 255, cv2.THRESH_BINARY)[1]
    
    new = cv2.dilate(new, np.ones((9,3), np.uint8), iterations=5)
    
    _, contours, _ = cv2.findContours(new, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        
        
        if (((y + h) < (alturaJanela / 3)) &   (cv2.contourArea(contour) < 40*40) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            bg = atualizaBackground(x,y,w,h,bg,gray)
            
            continue
        
        if (((y + h) > (alturaJanela / 3)) & ((y + h) < ((alturaJanela / 3)) * 2) &   (cv2.contourArea(contour) < ((40*40)*2)) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            bg = atualizaBackground(x,y,w,h,bg,gray)
            
            continue
        
        if (((y + h) > ((alturaJanela / 3)) * 2) &   (cv2.contourArea(contour) < ((40*40)*3)) & (w < (h * 4)) & (w > (h * 0.20)) ):
            
            bg = atualizaBackground(x,y,w,h,bg,gray)
            
            continue
        
        
        if cv2.contourArea(contour) < 60*60:
            continue
        
        
        
        color = (0, 255, 0)
        
        salva = True
        for nitem in range(0, len(lista)):
            
            item = lista[nitem]
            
           
            
            if(item.verificaArea(x, y, w, h)):
                
                salva = False
                #indices(0:x,1:y,2:w,3:h,4:numero do quadrado,5:posição do quadro no frame anterior,6:informa se é uma pessoa)
                #novoitem = objeto.Objeto(item.num,x, y, w, h,[item.x,item.y,item.w,item.h],item.verificacoes,item.confirmado,item.ultimoMovimento, item.deteccoes)
                #[x, y, w, h, item[4],[item[0],item[1],item[2],item[3]],item[6]]
                
                if(item.ultimoFrame == numFrame):
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
                item.ultimoFrame = numFrame
                
                #lista.pop(nitem)
                
                #lista.insert(nitem,novoitem)
                
                
                continue
            
        
            
        
        #se o quadrado não estiver na lista salva ele
        if(salva):
            lista.append(Objeto(x, y, w, h,[x, y, w, h],time.time(),numFrame,gray))
            
            #lista.append([x, y, w, h,numFrame ,[x, y, w, h],False])
            
            
    
    
    
    
    
             
        
        
    
    #a cada 5 frames verifica por quadrados duplicados
    if(numFrame % 5 == 0):
        
        num1 = 0;
        num2 = 0;
        while num1 < len(lista):
            
            if(lista[num1].w * lista[num1].h >= ((larguraJanela * alturaJanela) * 0.9)):
                
                
                primarybg = cv2.cvtColor(pegarBackground(video_capture), cv2.COLOR_BGR2GRAY);
                
                bg = primarybg.copy()
                
                
                
                
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
                cv2.putText(frame, "{}".format("SOS"), (x, y+250), cv2.FONT_HERSHEY_SIMPLEX, 3, color, 3)
               
            if((item.tempoParado() > 10) & (item.pessoa() == False)):
                bg = atualizaBackground(item.x,item.y,item.w,item.h,bg,gray)         
                            
        else:
            item.ultimoMovimento = time.time()
        
    #Marca quadrados na imagem
    for nitem in range(0, len(lista)):
        
        item = lista[nitem]
        
        x = item.x
        y = item.y
        w = item.w
        h = item.h
        
        
            
        
        cv2.putText(frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
        cv2.putText(frame, "{}".format(str(item.ultimoMovimento)), (x, y+180), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        if(item.pessoa()):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50,200,50), 2)
        
    
    
        
    frameShow = frame
    #show(new,bg,frame)
    
    #show = threading.Thread(target=show,args=(new,bg,frame,))
    #show.start()
    
    
    if(numFrame % 5 == 0):
        nitem = 0
        while(nitem < len(lista)):
            if(lista[nitem].ultimoFrame < numFrame - 2):
                lista[nitem].stopObjeto()
                lista.pop(nitem)
            else:
                nitem = nitem + 1
    
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('n'):     
        cv2.destroyAllWindows()
        
        primarybg = cv2.cvtColor(pegarBackground(video_capture), cv2.COLOR_BGR2GRAY);
        
        bg = primarybg.copy();
        
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
video_capture.release()
cv2.destroyAllWindows()

