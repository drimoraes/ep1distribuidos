import threading
import re 
import sys
from message import Message


class HandlerReceive:
    def __init__(self, peer):
        self.peer = peer

    def escutar(self):
        self.peer.socket_listen.listen(5) 
        print("Escutando por conexões...")

        while True:
            conn, addr = self.peer.socket_listen.accept() 
            # Usamos threads para tratar cada requisição
            threading.Thread(target=self.tratarReq, args=(conn, addr), daemon=True).start()

    def tratarReq(self, conn, addr):
        data = conn.recv(1024)

        try:
            data_str = data.decode('utf-8')  # Decodifica os dados para string
            origem, clock, tipo, argumentos = Message.processarMensagem(data_str)

            # Identifica o comando recebido
            if tipo == "HELLO":
                self.handleHello(origem, clock)
            elif tipo == "GET_PEERS":
                self.handleGetPeers(conn, origem, clock, tipo)
            elif tipo == "LIST_FILES":
                self.handleListFiles(origem, clock)
            elif tipo == "BYE":
                self.handleBye(origem,clock)
            else:
                print(f"Tipo {tipo} desconhecido.")

        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    def handleHello(self, origem, clock):
        print(f"Mensagem recebida: {origem} {clock} HELLO")
        self.peer.attClock()
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        print(">")
    
    def handleBye(self, origem, clock):
        print(f"Mensagem recebida: {origem} {clock} BYE")
        self.peer.attClock()
        clock = self.peer.getClock()
        print (f"=> Atualizando relógio para: {clock}")
        self.peer.atualizar_status_peer(origem, "OFFLINE")
        print(">")
        
 
    def handleGetPeers(self, conn, origem, clock, tipo):
        print(f"Mensagem recebida: {origem} {clock} {tipo}")
        self.peer.attClock()
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        Message.mensagemPeerList(self.peer, origem, self.peer.getClock(), conn)
        print(">")
        
    def handlePeersList(self, conn):
        data = conn.recv(1024).decode()
        origem, clock, tipo, argumentos = Message.processarMensagem(data)
        arg_formatados = ' '.join(argumentos)
        print(f"Resposta recebida: {origem} {clock} {tipo} {arg_formatados}")
        self.peer.attClock()
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        for peer in range(1, (int(argumentos[0]) + 1)):
            ip, porta, status,num = argumentos[peer].split(':')
            peerAdd = ip + ':' + porta
            self.peer.adicionar_novo_peer(peerAdd, status)
            

