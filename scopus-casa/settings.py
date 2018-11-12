# -*- coding: utf-8 -*-
class Settings(object):
    
    ANGULO_CAMERA_0 = 0
    ANGULO_CAMERA_90 = 90
    ANGULO_CAMERA_180 = 180
    ANGULO_CAMERA_270 = 270
    
    SAIDA_CASA = 0
    SAIDA_COMODO = 1
    SAIDA_BANHEIRO = 2
    
    COMODO_VAZIO = 0
    OBJETO_NO_COMODO = 1
    PESSOA_NO_COMODO = 2
    ALERTA_RISCO = 3
    SAIU_DA_CASA = 4
    PODE_ESTAR_NO_BANHEIRO = 5
    
    def __init__(self):
        
        self.cliente = "wesley@"
        
        self.cameras = [    #Lista de cameras
                [ 
                    "1",    #ID da camera
                    "Sala",     #Nome do comodo
                    "rtsp://192.168.1.109:554/user=admin&password=raspcam&channel=1&stream=0.sdp?",     #IP da camera
                    Settings.ANGULO_CAMERA_270,   #Angulo da camera
                    1,    #proporção da imagem - 1 = largura e altura original, 0.5 metade da largura e metade da altura original
                    [   #Lista de areas seguras (coordenadas considerando a porcentagen do tamanho da tela)
                        [1,21,40,77]
                    ],
                    [   #Lista de areas seguras (coordenadas considerando a porcentagen do tamanho da tela)
                        [Settings.SAIDA_CASA,[35,0,55,60]],
                        [Settings.SAIDA_BANHEIRO,[0,15,62,85]]
                    ]
                ]#,
#                 [ 
#                    "2",     #ID da camera
#                     "Quarto Rita",      #Nome do comodo
#                     "rtsp://192.168.1.110:554/user=admin&password=raspcam&channel=1&stream=0.sdp?",     #IP da camera
#                     Settings.ANGULO_CAMERA_270,     #Angulo da camera
#                     1,    #proporção da imagem - 1 = largura e altura original, 0.5 metade da largura e metade da altura original
#                     [   #Lista de areas seguras (coordenadas considerando a porcentagen do tamanho da tela)
#                         [0,0,35,100]
#                     ],
#                     [   #Lista de areas seguras (coordenadas considerando a porcentagen do tamanho da tela)
#                         
#                     ]
#                 ]
            ]   
        
        
        
        
        self.areaMinimaParaBg = 40*40   #Area minima para que um quadrado seja incluido no Backgtround
        self.areaMinimaParaLista = 70*70    #Area minima para que um quadrado seja incluido na Lista de Objetos ou pessoas
        self.framesVerificaQadrados = 5     #intervalo em frames para verificação de quadrados que não tem mais objetos, ou quadrados repetidos, ou muito grandes
        self.proporcaoQuadradoTelaParaBg = 0.9      #proporção entre um quadrado e a tela para considerar que deve trocar todo o Background
        self.variacaoMovimento = 5      #numero de pixel que podem  variar para que ainda considere algo parado 
        
        self.tempoParaAlerta = 5    #Tempo em segundos que o idoso deve ficar parado para ativar o alerta
        
        self.tempoParaMoverObjeto = 5   #Tempo em segundos que um objeto deve ficar parado para ser carregado no background
        
        self.limpaBgTime = 10   #tempo em segundos entre cada limpeza do background
        self.limpaBgSensibilidade = 10      #sensibilidade para identificar mudanças da imagem atual para o background (0 - 255), quanto menor mais sensivel
        
        self.pegarBgSensibilidade = 10      #sensibilidade para identificar mudanças entre as imagens (0 - 255), quanto menor mais sensivel
        self.pegarBgTentativas = 100    #numero de tentativas de leitura do ambiente antes de pegar partes das imagens guardadas 
        self.pegarContornosSensibilidade = 60   #sensibilidade para identificar mudanças da imagem atual para o background para criar objetos (0 - 255), quanto menor mais sensivel, porem cria objetos para mais sombras
        self.aguardeBgTime = 200    #caso exceda o numero de tentativas de leitura do ambiente o sistema vai aguardar esse tempo em segundos sem movimentos no ambiente para tentar pegar o background novamente
        
        self.objetoDeteccoes = 200     #tamanho do histórico de detecções de pessoa que deve ser guardado
        self.objetoMinDeteccoes = 10     #quantidade de detecções que tem que ser positivas para pessoa no histórico para considerar o objeto uma pessoa
        self.objetoProporcaoArea = 0.15    #O quanto de um quadrado deve estar dentro do outro para considerar o mesmo quadrado (0 - 1)
        
        
        self.serverHost = "192.168.1.105"
        self.serverPort = 5000
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        