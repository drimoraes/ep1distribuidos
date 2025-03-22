import socket
import threading
import sys
import os
from receiveHandler import HandlerReceive
from sendHandler import SendReceive

class Peer: 
    def __init__(self, enderecoTotal, arq, diretorio):
        self.ip, self.porta = enderecoTotal.split(":")
        self.porta = int(self.porta)
        self.clock = 0
        print(f"IP: {self.ip}, PORT: {self.porta}")  # Verificando IP e PORT
        self.arquivo = arq
        self.peerdir = diretorio
        receive = HandlerReceive(self, self.clock)  
        send = SendReceive(self.ip, self.porta)      
        self.verificaDir(self.peerdir)
        self.carregarPeers(arq) # essa funcao deve usar o bgl de abrir arquivos
        self.criasocket(self.ip, self.porta)
        self.escutar(self.socket)
        
    def verificaDir(self, dir):
        if not (os.path.isdir(dir) and os.access(dir, os.R_OK)):
            print("Erro: O diretório não existe ou não tem permissão de leitura.")
            sys.exit(1)
            
    def carregarPeers(self, arqpeers):
        print("ok")
        
    def criasocket(self, ip, porta):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, porta))
        print(f"Socket criado e vinculado a {ip}:{porta}")
        
    def escutar(self):
        threading.Thread(target=self.receive.escutar, daemon=True).start()
        
    def attClock(self):
        self.clock += 1
        
    def getClock(self):
        return self.clock
    
    def getIP(self):
        return self.ip
    
    def getPorta(self):
        return self.porta
    
    def atualizarStatus(self, peer_destino, status):
        
        print(f"Atualizando peer {peer_destino} status {status}")
        self.peers[peer_destino] = status