# -*- coding: utf-8 -*-

import socket
import errno
import time
import threading 
from settings import Settings

class Status(object):
    
    
    def __init__(self):
        self.comodos = []
        
        self.settings = Settings()
        
        self.stop = False
        
        self.tcp = None
        
        
        self.carregaStatusthr = threading.Thread(target=(self.carregaStatus),args=())
        self.carregaStatusthr.start()
    
    
    def novoComodo(self,comodo,status,frame):
        item = [comodo,status,frame,-1]
        self.comodos.append(item)
        return self.comodos.index(item)
        
        
        
    def carregaStatus(self):
        time.sleep(3)
        
        
        self.conectaSocket()
        
        
        
        time.sleep(12)
        
        
        while(not self.stop):
            time.sleep(0.5)
            
            text = ""
            for comodo in self.comodos:
                if(comodo[1] != comodo[3]):
                    comodo[3] = comodo[1]
                    text = '{"comodo":"'+comodo[0]+'","estado":'+str(comodo[1])+'}'
                    
                    text2 = "\n"+comodo[0]+": "
                    
                    
                    if(comodo[1] == self.settings.COMODO_VAZIO ):
                        text2 += "comodo vazio";
                    elif(comodo[1] == self.settings.OBJETO_NO_COMODO ):
                        text2 += "objeto no comodo"
                    elif(comodo[1] == self.settings.PESSOA_NO_COMODO ):
                        text2 += "pessoa no comodo"
                    elif(comodo[1] == self.settings.ALERTA_RISCO ):
                        text2 += "ALERTA DE RISCO"
                    elif(comodo[1] == self.settings.SAIU_DA_CASA ):
                        text2 += "saiu da casa"
                    elif(comodo[1] == self.settings.PODE_ESTAR_NO_BANHEIRO ):
                        text2 += "pode estar no banheiro"
                        
                    
                    enviar = True
                    
                    while(enviar):
                        try:
                            self.tcp.send(str(len(text)).zfill(3))
                            self.tcp.send(text)
                            enviar = False
                        except socket.error as e:
                            print("Erro ao enviar estado de :"+comodo[0]+"  :",e)
                            if e.errno == errno.EPIPE:
                                self.tcp.close()
                                self.conectaSocket()
                                
                    print(text2)
                
    
    
    def setStatusComodo(self,indice, status,frame):
        self.comodos[indice][1] = status
        self.comodos[indice][2] = frame
    
    
    def getFrameComodo(self,indice):
        return self.comodos[indice][2]
    
    
    def getStatusComodo(self,indice):
        return self.comodos[indice][1]
    
    
    
    def conectaSocket(self):
        
        conected = False
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (self.settings.serverHost, self.settings.serverPort)
        
        while(not conected): 
            try:
                self.tcp.connect(dest)
                conected = True
            except socket.error as e:
                print("Erro ao conectar ::%s",e)
                time.sleep(5)
            
            
        self.tcp.send("1")
        self.tcp.send(str(len(self.settings.cliente)).zfill(3))
        self.tcp.send(self.settings.cliente)
        
    
    
    
    
    
    
    
    
    
    
    
    