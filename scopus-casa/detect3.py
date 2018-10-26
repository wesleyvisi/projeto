# -*- coding: utf-8 -*-
import socket
import numpy as np
import cv2
import time
import sys
from objeto import Objeto
from imagens import Imagens
import threading 
import datetime 
from datetime import date





def show(imagens,lista):
    time.sleep(1)
    while True:
        
        if(not imagens.pegandoBackground):
            time.sleep(0.2)
            cv2.imshow("bin",imagens.bin)
            cv2.imshow("bg",imagens.bg)
            cv2.imshow("Frame",imagens.frameShow)
            #cv2.imshow("primary",imagens.primarybg)
            
            waitKey = cv2.waitKey(1) 
            if waitKey & 0xFF == ord('q'):  
                cv2.destroyAllWindows()
                imagens.stopImagens()
                for item in lista:
                    item.stopObjeto()
                continua = False
                break
            
            if waitKey & 0xFF == ord('n'):     
                cv2.destroyAllWindows()
                imagens.pegarBackground()
        





print("carregando... ")
imagens = Imagens("rtsp://192.168.1.109:554/user=admin&password=raspcam&channel=1&stream=0.sdp?",270,1)
#imagens = Imagens(0,0,1)
#datetime.datetime.now()




HOST = '192.168.1.104'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
tcp.send("1")
continua = True

lista = []


show = threading.Thread(target=show,args=(imagens,lista,))
show.start()

while continua:
    
    if(imagens.pegandoBackground == False):
        
        imagens.readFrame()
        
        contours = imagens.pegarContornos()
        
        
        for contour in contours:
            
            (x, y, w, h) = cv2.boundingRect(contour)
            
            
            
            
            color = (0, 255, 0)
            
            salva = True
            for nitem in range(0, len(lista)):
                
                if(not salva):
                    break
                    
                    
                item = lista[nitem]
                
                area = item.verificaArea(x, y, w, h)
                
#                 if (((((y + h) < (imagens.alturaImagem / 3)) &   (cv2.contourArea(contour) < 35*35) & (w < (h * 4)) & (w > (h * 0.20)) )  |
#                     (((y + h) > (imagens.alturaImagem / 3)) & ((y + h) < ((imagens.alturaImagem / 3)) * 2) &   (cv2.contourArea(contour) < ((35*35)*2)) & (w < (h * 4)) & (w > (h * 0.20)) )  |
#                     (((y + h) > ((imagens.alturaImagem / 3)) * 2) &   (cv2.contourArea(contour) < ((35*35)*3)) & (w < (h * 4)) & (w > (h * 0.20)) )
#                     ) & (not area)):
#                     salva = False
#                     imagens.atualizaBackground(x,y,w,h)
#                     
#                     continue
                
                if((cv2.contourArea(contour) < 40*40) & (w < (h * 4)) & (w > (h * 0.20)) & (not area)):
                    salva = False
                    imagens.atualizaBackground(x,y,w,h)
                    
                    break
                
                if(cv2.contourArea(contour) < 50*50):
                    break
                
                
                    
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
                    else:
                        item.areaAnterior = [item.x,item.y,item.w,item.h]
                            
                        
                    item.x = x
                    item.y = y
                    item.w = w
                    item.h = h
                    item.ultimoFrame = imagens.numFrame
                    
                    
                    break
                
            
                
            
            #se o quadrado não estiver na lista salva ele
            if(salva & (cv2.contourArea(contour) > 70*70)):
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
            variacao = 5 #(((imagens.larguraImagem + imagens.alturaImagem) /2) * 0.01)
            print("variação "+str(variacao))
            #if((item.x >= (item.areaAnterior[0] - (item.w * 0.02))) & (item.x <= (item.areaAnterior[0] + (item.w * 0.02))) & (item.y >= (item.areaAnterior[1] -(item.h * 0.02))) & (item.y <= (item.areaAnterior[1] + (item.h * 0.02)))   &   (item.w >= (item.areaAnterior[2] - (item.w * 0.02))) & (item.w <= (item.areaAnterior[2] + (item.w * 0.02))) & (item.h >= (item.areaAnterior[3] - (item.h * 0.02))) & (item.h <= (item.areaAnterior[3] + (item.h * 0.02))) ):
            if((item.x <= (item.areaAnterior[0] - variacao)) |
                (item.x >= (item.areaAnterior[0] + variacao)) |
                 (item.y <= (item.areaAnterior[1] - variacao)) |
                  (item.y >= (item.areaAnterior[1] + variacao)) |
                   (item.w <= (item.areaAnterior[2] - variacao)) |
                    (item.w >= (item.areaAnterior[2] + variacao)) |
                     (item.h <= (item.areaAnterior[3] - variacao)) |
                      (item.h >= (item.areaAnterior[3] + variacao)) ):
                #print("x " + str(item.x)+" , "+str( item.areaAnterior[0])+" -  y "+str(item.y)+" , "+str( item.areaAnterior[1] )+" -  w "+str(item.w)+" , "+str( item.areaAnterior[2])+" -  h "+str(item.h)+" , "+str( item.areaAnterior[3] ) )
                item.ultimoMovimento = time.time()        
             
                
            
        #Marca quadrados na imagem
        if(len(lista) == 0):
            tcp.send("0")
        for nitem in range(0, len(lista)):
            
            item = lista[nitem]
            
            x = item.x
            y = item.y
            w = item.w
            h = item.h
            
            
                
            
            #cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
            #cv2.putText(imagens.frame, "{}".format(str(int(time.time() - item.ultimoMovimento))), (x, y+110), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            if((item.pessoa()) & (item.tempoParado() > 8)):
                cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 2)
                cv2.putText(imagens.frame, "{}".format("SOS"), (x, y+120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 10)
                cv2.rectangle(imagens.frame, (x, y), (x + w, y + h), (0,0,255), 3)
                tcp.send("3")
                
            elif(item.pessoa() ):
                cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
                cv2.putText(imagens.frame, "{}".format(str(int(item.tempoParado()))), (x, y+120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,255), 3)
                cv2.rectangle(imagens.frame, (x, y), (x + w, y + h), (0,255,0), 3)
                tcp.send("1")
                
            elif(item.tempoParado() > 8):
                imagens.atualizaBackground(item.x,item.y,item.w,item.h)  
                tcp.send("2")
            else:
                cv2.putText(imagens.frame, "{}".format(str(item.num)), (x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50,255,255), 2)
                cv2.rectangle(imagens.frame, (x, y), (x + w, y + h), (50,255,255), 3)
                tcp.send("2")
            
        
        
            
        imagens.atualizaFrameShow()
    
    
        
        
        if(imagens.numFrame % 5 == 0):
            nitem = 0
            while(nitem < len(lista)):
                if(lista[nitem].ultimoFrame < imagens.numFrame - 2):
                    lista[nitem].stopObjeto()
                    lista.pop(nitem)
                else:
                    nitem = nitem + 1
        
        
        
    
    
    
    
video_capture.release()
cv2.destroyAllWindows()

