from _ast import Num
import time

class Objeto(object):
    

    
    def __init__(self, num, x, y, w, h, areaAnterior, verificacoes, confirmado, tempo, deteccoes):
        self.num = num
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.areaAnterior = areaAnterior
        self.verificacoes = verificacoes
        self.confirmado =  confirmado
        self.ultimoMovimento = tempo
        self.deteccoes = deteccoes
        
        
    def tempoParado(self):
        return time.time() - self.ultimoMovimento
    
    
    def deteccoesAdd(self, r):
        self.deteccoes.append(r)
        if(len(self.deteccoes) > 200):
            self.deteccoes.pop(0)
    
    
    def pessoa(self):
        
        pessoa = 0 
        
        for item in self.deteccoes:
            if(item):
                pessoa = pessoa + 1
        
        if(pessoa > (len(self.deteccoes) / 50)):
            return True
        else: 
            return False
            
            
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        