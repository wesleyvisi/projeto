import socket
import numpy as np
import cv2
import threading 
import time 
from conexoes import Conexoes






def receberEEnviar(casa,celulares):
    ativo = True
    data = ""
    erros = 0
    while ativo:
        
        tamanho = casa[1].recv(3)
            
        if(tamanho != ""):
        
            
            data = casa[1].recv(int(tamanho))
            
            if(data != ""):
                erros = 0
            else:
                erros = erros + 1
        else:
            erros = erros + 1
        
        
        if(erros > 10):
            casa[1].close()
            print(casa[0]+".close()")
            ativo = False
            
         
        if(data != ""):
            
            celularesLen = len(celulares)
            i = 0
            while(i < celularesLen):
                celular = celulares[i]
                            
                    
                if(casa[0] == celular[0] ):
                    
                    
                    
                    try:       
                        celular[1].send(data+"\n");
                    except socket.error as e:
                        celular[1].close()
                        print(celular[0]+".close()")
                        print("Erro ao enviar estado")
                        celulares.pop(i)
                        celularesLen = celularesLen - 1
                        i = i - 1
                        
                i = i + 1
            
            
            for i in range(0,len(celulares)):
                celular = celulares[i]
                            
                    
                if(casa[0] == celular[0] ):
                    print(data)
                    print(celular[0])
                    
                    
                    try:       
                        celular[1].send(data+"\n");
                    except socket.error as e:
                        celular[1].close()
                        print(celular[0]+".close()")
                        print("Erro ao enviar estado")
                        celulares.pop(i)
                        time.sleep(0.5)
                        
    

def aceitaClientes(celulares,casas):
    while True:
        
        conexao, cliente = tcp.accept()
        tipo = conexao.recv(1)
        tamanho = conexao.recv(3)
        user = conexao.recv(int(tamanho))
        
        
        if(int(tipo) == 1):
            casa = [user,conexao,cliente,0]
            
            
            casa[3] = threading.Thread(target=(receberEEnviar),args=(casa,celulares))
            casa[3].start()
            
            casas.append(casa)
            print('Casa - Conectado por',user, cliente)
            
            
        if(int(tipo) == 2):
            
            celulares.append([user,conexao,cliente])
            print('celular - Conectado por',user, cliente)
            
            
            
        
             





HOST = '192.168.1.105'              # Endereco IP do Servidor      # Porta que o Servidor esta
PORT = 5000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.bind(dest)
tcp.listen(1)

print(tcp.getsockname())


celulares = []
casas = []

aceitaClientesthr = threading.Thread(target=(aceitaClientes),args=(celulares,casas))
aceitaClientesthr.start()




            
    
    
    
    
   