from _ast import Num

class Objeto(object):
    

    
    def __init__(self, num, x, y, w, h, areaAnterior, verificacoes, confirmado, tempo):
        self.num = num
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.areaAnterior = areaAnterior
        self.verificacoes = verificacoes
        self.confirmado =  confirmado
        self.ultimoMovimento = tempo
        
        