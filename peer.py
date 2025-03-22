import socket
import threading
import sys
import os
from receiveHandler import HandlerReceive
from sendHandler import SendReceive
from PeerListHandler import PeerListHandler


class Peer: 
    def __init__(self, enderecoTotal, arq, diretorio):
        self.ip, self.porta = enderecoTotal.split(":")
        self.porta = int(self.porta)
        self.clock = 0
        print(f"IP: {self.ip}, PORT: {self.porta}")  # Verificando IP e PORT
        self.arquivo = arq
        self.peerdir = diretorio
        self.receive = HandlerReceive(self, self.clock)  
        self.send = SendReceive(self.ip, self.porta)      
        self.peers_handler = PeerListHandler() 
        self.verificaDir(self.peerdir)
        self.criasocket(self.ip, self.porta)
        self.escutar(self.socket)
        
    def verificaDir(self, dir):
        if not (os.path.isdir(dir) and os.access(dir, os.R_OK)):
            print("Erro: O diretório não existe ou não tem permissão de leitura.")
            sys.exit(1)
            
    def carregar_peers(self, arq):
        self.peers_handler.carrega_peers(arq)

    def atualizar_status_peer(self, peer, novo_status):
        self.peers_handler.atualizar_status(peer, novo_status)

    def adicionar_novo_peer(self, peer):
        self.peers_handler.adicionar_peer(peer)

    def buscar_peer(self, peer):
        return self.peers_handler.busca_peer(peer)
             

    def criasocket(self, ip, porta):
        #chat sugeriu colocar apenas self.escutar()
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
    
