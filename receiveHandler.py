import threading
import re 
import sys
from message import Message


class HandlerReceive:
    def __init__(self, peer: "Peer"):
        self.peer = peer

    def escutar(self):
        # Usa o socket de escuta criado na classe Peer
        self.peer.socket_listen.listen(4)  # Inicia a escuta para até 4 conexões simultâneas
        print("Escutando por conexões...")

        while True:
            # Aceita conexões de clientes
            conn, addr = self.peer.socket_listen.accept()  # Espera uma nova conexão
            #print(f"Conexão recebida de {addr}")
            # Cria uma nova thread para tratar a requisição
            threading.Thread(target=self.tratarReq, args=(conn, addr), daemon=True).start()

    def tratarReq(self, conn, addr):
        # Identifica o código da mensagem
        data = conn.recv(1024)

        try:
            data_str = data.decode('utf-8')  # Decodifica os dados para string
            origem, clock, tipo, argumentos = Message.processarMensagem(data_str)

            # Executa diferentes lógicas dependendo do TIPO
            if tipo == "HELLO":
                self.handleHello(origem, clock)
            elif tipo == "GET_PEERS":
                self.handleGetPeers(conn, origem, clock, tipo, argumentos)
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
        sys.exit(0) 
        

    def handleGetPeers(self, conn, origem, clock, tipo, argumentos):
        print(f"Mensagem recebida: {origem} {clock} {tipo}")
        self.peer.attClock()
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        Message.mensagemPeerList(self.peer, origem, self.peer.getClock(), conn, argumentos)
        
    def handlePeersList(self, conn):
        data = conn.recv(1024).decode()
        origem, clock, tipo, argumentos = Message.processarMensagem(data)
        print(f"argumentos {argumentos}")
        print(f"Mensagem recebida: {origem} {clock} {tipo}")
        self.peer.attClock()
        print(f"Atualizando relógio para {self.peer.getClock()}")
        self.peer.atualizar_status_peer(origem, "ONLINE")
        for peer in range(1, (int(argumentos[0]) + 1)):
            ip, porta, status,num = argumentos[peer].split(':')
            peerAdd = ip + ':' + porta
            self.peer.adicionar_novo_peer(peerAdd, status)
            


    def handleListFiles(self, origem, clock):
        print(f"Mensagem recebida: {origem}, {clock}, LIST_FILES")
        # Lógica para lidar com LIST_FILES

#    def processarMensagem(self, data_str):
#        match = re.match(r"(\S+)\s+(\S+)\s+(\S+)\s*(.*)", data_str)

        #if match:
         #   origem = match.group(1)
          #  clock = match.group(2)
          #  tipo = match.group(3)
          #  argumentos = match.group(4).split() if match.group(4) else []  # Se não houver argumentos, retorna lista vazia
            
          #  return origem, clock, tipo, argumentos
        #else:
            # Se a correspondência falhar, retornamos None para os valores
         #   print("Erro: formato de mensagem inválido.")
          #  return None, None, None, None

