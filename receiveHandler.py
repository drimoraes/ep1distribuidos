import threading
import re 
import sys
from message import Message
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from peer import Peer

class HandlerReceive:
    def __init__(self, peer: "Peer"):
        self.peer = peer

    def recv_completo(self, conn):
        buffer = ""
        while True:
            dados = conn.recv(1024).decode("utf-8")
            if not dados:
                break  # conexão foi encerrada
            buffer += dados
            if '\n' in buffer:
                break  # fim da mensagem detectado
        return buffer.strip()

    def escutar(self):
        self.peer.socket_listen.listen(5) 
        print("Escutando por conexões...")

        while True:
            conn, addr = self.peer.socket_listen.accept() 
            threading.Thread(target=self.tratarReq, args=(conn, addr), daemon=True).start()

    def tratarReq(self, conn, addr):
        data_str = self.recv_completo(conn)

        try:
            origem, clock, tipo, argumentos = Message.processarMensagem(data_str)

            if tipo == "HELLO":
                self.handleHello(origem, clock)
            elif tipo == "GET_PEERS":
                self.handleGetPeers(conn, origem, clock, tipo)
            #elif tipo == "LIST_FILES":
            #    self.handleListFiles(origem, clock)
            elif tipo == "BYE":
                self.handleBye(origem, clock)
            elif tipo == "LS":
                self.handleLS(conn, origem, clock, tipo)
            elif tipo == "LS_LIST":
                self.handleLSList(conn, origem, clock, tipo)
            elif tipo == "DL":
                self.handleDL(conn, origem, clock, tipo, argumentos)
            else:
                print(f"Tipo {tipo} desconhecido.")

        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    def handleHello(self, origem, clock):
        print(f"Mensagem recebida: {origem} {clock} HELLO")
        localClock = self.peer.getClock()
        newclock = max(localClock, int(clock))
        self.peer.attClock2(newclock)

        clocklista = self.peer.returnClock(origem)
        newClockLista = max(int(clocklista), int(clock))
        self.peer.atualizaClock(origem, newClockLista)

        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        print(">")

    def handleBye(self, origem, clock):
        print(f"Mensagem recebida: {origem} {clock} BYE")
        localClock = self.peer.getClock()
        newclock = max(localClock, int(clock))
        self.peer.attClock2(newclock)
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "OFFLINE")
        print(">")

    def handleGetPeers(self, conn, origem, clock, tipo):
        print(f"Mensagem recebida: {origem} {clock} {tipo}")
        localClock = self.peer.getClock()
        newclock = max(localClock, int(clock))
        self.peer.attClock2(newclock)

        clocklista = self.peer.returnClock(origem)
        newClockLista = max(int(clocklista), int(clock))
        self.peer.atualizaClock(origem, newClockLista)

        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        Message.mensagemPeerList(self.peer, origem, self.peer.getClock(), conn)
        print(">")
        

    def handlePeersList(self, conn):
        data_str = self.recv_completo(conn)
        origem, clock, tipo, argumentos = Message.processarMensagem(data_str)
        arg_formatados = ' '.join(argumentos)
        print(f"Resposta recebida: {origem} {clock} {tipo} {arg_formatados}")
        
        localClock = self.peer.getClock()
        newclock = max(localClock, int(clock))
        self.peer.attClock2(newclock)
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")

        clocklista = self.peer.returnClock(origem)
        newClockLista = max(int(clocklista), int(clock))
        self.peer.atualizaClock(origem, newClockLista)
        
        for peer in range(1, (int(argumentos[0]) + 1)):
            ip, porta, status, num = argumentos[peer].split(':')
            peerAdd = ip + ':' + porta
            clockmsg = int(num)
            self.peer.adicionar_novo_peer2(peerAdd, status, clockmsg)
            
    def handleLS(self, conn, origem, clock, tipo):
        print(f"Mensagem recebida: {origem} {clock} {tipo}")
        localClock = self.peer.getClock()
        newclock = max(localClock, int(clock))
        self.peer.attClock2(newclock)

        clocklista = self.peer.returnClock(origem)
        newClockLista = max(int(clocklista), int(clock))
        self.peer.atualizaClock(origem, newClockLista)

        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        Message.mensagemLSList(self.peer, origem, self.peer.getClock(), conn)
        print(">")
        
    def handleLSList(self, conn):
        data_str = self.recv_completo(conn)
        origem, clock, tipo, argumentos = Message.processarMensagem(data_str)
        arg_formatados = ' '.join(argumentos)
        print(f'Resposta recebida: "{origem} {clock} {tipo} {arg_formatados}"')
        
        localClock = self.peer.getClock()
        newclock = max(localClock, int(clock))
        self.peer.attClock2(newclock)
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        
        for arq in range(1, (int(argumentos[0]) + 1)):
            nome, tam = argumentos[arq].split(':')
            self.peer.adicionar_novo_arq_encontrado(nome, tam, origem)
        
        self.peer.exibeArquivosEncontrados()


    def handleDL(self, conn, origem, clock, tipo, args):
        arg_formatados = ' '.join(args)
        print(f"Mensagem recebida: {origem} {clock} {tipo} {arg_formatados}")
        localClock = self.peer.getClock()
        newclock = max(localClock, int(clock))
        self.peer.attClock2(newclock)

        clocklista = self.peer.returnClock(origem)
        newClockLista = max(int(clocklista), int(clock))
        self.peer.atualizaClock(origem, newClockLista)

        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")

        nomearq = args[0]
        Message.mensagemFILE(self.peer, origem, self.peer.getClock(), conn, nomearq)
        print(">")


    def handleFILE(self, conn):
        data_str = self.recv_completo(conn)
        origem, clock, tipo, argumentos = Message.processarMensagem(data_str)
        arg_formatados = ' '.join(argumentos)
        print(f"Resposta recebida: {origem} {clock} {tipo} {arg_formatados}")
        
        localClock = self.peer.getClock()
        newclock = max(localClock, int(clock))
        self.peer.attClock2(newclock)
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")

        self.peer.baixarArq(argumentos[0], argumentos[3])
