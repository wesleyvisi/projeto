# -*- coding: utf-8 -*-

import numpy as np
import cv2
import time
import sys
import objeto
import threading 



def verificaArea(q1,q2):
    x1 = q1[0]
    y1 = q1[1]
    w1 = q1[2]
    h1 = q1[3]
    
    x2 = q2[0]
    y2 = q2[1]
    w2 = q2[2]
    h2 = q2[3]
    
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
    
    if((A > (A1 * 0.25)) | (A > (A2 * 0.25))):
        return True
    
    else:
        return False

            
          
         


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


def detecta():
    while True:
        time.sleep(0.1)
        for nitem in range(0, len(lista)):
            
            item = lista[nitem]
            
            x = item.x
            y = item.y
            w = item.w
            h = item.h
            
            #se o quadrado ainda não foi confirmado como pessoa, verifica utilizando Cascade se encontra a parte de cima de uma pessoa somente dentro do quadro
            if(numFrame % 2 == 0):
                quadro = gray[y:y+h, x:x+w]

                frontalFaces = frontalFaceCascade.detectMultiScale(quadro, scaleFactor=1.2, minNeighbors=3)
                
                if(len(frontalFaces) > 0):
                    item.deteccoesAdd(True)
                else:
                    upperbodys = upperbodyCascade.detectMultiScale(quadro, scaleFactor=1.2, minNeighbors=3)
                    if(len(upperbodys) > 0):
                        item.deteccoesAdd(True)
                    else:
                        fullbodys = fullbodyCascade.detectMultiScale(quadro, scaleFactor=1.2, minNeighbors=4)
                        if(len(fullbodys) > 0):
                            item.deteccoesAdd(True)
                        else:
                            item.deteccoesAdd(False)
                    
                    
                
                
                item.verificacoes = item.verificacoes + 1
                
def show():
    time.sleep(3)
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
video_capture = cv2.VideoCapture("rtsp://10.42.0.96:554/user=admin&password=raspcam&channel=1&stream=0.sdp?")
#video_capture = cv2.VideoCapture(0)

#video_capture.set(5, 1)


cascPathUpperBody = "haarcascade_upperbody.xml"
cascPathFullBody = "haarcascade_fullbody.xml"
cascPathFrontalFace = "haarcascade_frontalface_default.xml"
upperbodyCascade = cv2.CascadeClassifier(cascPathUpperBody)
fullbodyCascade = cv2.CascadeClassifier(cascPathFullBody)
frontalFaceCascade = cv2.CascadeClassifier(cascPathFrontalFace)

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
detecta = threading.Thread(target=detecta,args=())
#detecta.start()

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
                
                
                item.areaAnterior = [item.x,item.y,item.w,item.h]
                item.x = x
                item.y = y
                item.w = w
                item.h = h
                item.ultimoFrame = numFrame
                
                #lista.pop(nitem)
                
                #lista.insert(nitem,novoitem)
                
                salva = False
                
                continue
            
        
            
        
        #se o quadrado não estiver na lista salva ele
        if(salva):
            lista.append(objeto.Objeto(numFrame,x, y, w, h,[x, y, w, h],time.time(),gray))
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
    
    
    if(len(contours) == 0):
        while(len(lista) > 0):
            lista.pop(0)
    
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('n'):     
        cv2.destroyAllWindows()
        
        primarybg = cv2.cvtColor(pegarBackground(video_capture), cv2.COLOR_BGR2GRAY);
        
        bg = primarybg.copy();
        
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
video_capture.release()
cv2.destroyAllWindows()

