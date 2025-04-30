import socket
import threading
import sys
import os
from receiveHandler import HandlerReceive
from sendHandler import HandlerSend
from PeerListHandler import PeerListHandler


class Peer: 
    def __init__(self, enderecoTotal, arquivotxt, diretorio):
        self.ip, self.porta = enderecoTotal.split(":")
        self.porta = int(self.porta)
        self.clock = 0
        self.arquivo = arquivotxt
        self.peerdir = diretorio
        self.arqEncontrados = {}
        self.receive = HandlerReceive(self)  
        self.send = HandlerSend(self)  
        self.peerslist = {"ONLINE": {}, "OFFLINE": {}}  
        self.peerslist_handler = PeerListHandler(self.peerslist) 
        self.verificaDir(self.peerdir)
        self.criar_socket_escuta()
        self.socket_send = None
        self.escutar()
        self.carregar_peers(arquivotxt)
        
    # Verifica se o diretório é valido
    def verificaDir(self, dir):
        if not (os.path.isdir(dir) and os.access(dir, os.R_OK)):
            print("Erro: O diretório não existe ou não tem permissão de leitura.")
            sys.exit(1)
    
    # Manipulação da lista de peers conhecidos usando o objeto da classe PeerListHandler encapsulado 
    def carregar_peers(self, arq):
        self.peerslist_handler.carrega_peers(arq)

    def atualizar_status_peer(self, peer, novo_status):
        self.peerslist_handler.atualizar_status(peer, novo_status)

    def adicionar_novo_peer(self, peer, status):
        self.peerslist_handler.adicionar_peer(peer, status)

    def buscar_peer(self, peer):
        return self.peerslist_handler.busca_peer(peer)
    
    def buscar_peerIP(self, peer):
        return self.peerslist_handler.busca_peerIP(peer)
    
    def tam_lista(self):
        return self.peerslist_handler.tamanho_lista()
    
    def lista_peersStatus(self, peerExcluido):
        return self.peerslist_handler.lista_peersStatus(peerExcluido)
    
    def returnClock(self, peer):
        return self.peerslist_handler.returnClock(peer)
    
    def atualizaClock(self, peer, clock):
        return self.peerslist_handler.atualizarClock(peer, clock)
        
             
    # Cria sockets para escutar comandos e enviar comandos
    def criar_socket_escuta(self):
        """Cria um socket para escutar conexões de outros peers."""
        self.socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_listen.bind((self.ip, self.porta))
        self.socket_listen.listen(5) # número escolhido arbitrariamente
        

    def criar_socket_envio(self, peer_destino):
        """Cria um socket para enviar mensagens para um peer específico."""
        try:
            ip_destino, porta_destino = peer_destino.split(":")
            porta_destino = int(porta_destino)

            self.socket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_send.connect((ip_destino, porta_destino))
            #print(f"Conectado ao peer {peer_destino}")

            return self.socket_send  # Retorna o socket de envio
        except (socket.error, ConnectionRefusedError) as e:
            print(f"Erro ao conectar com {peer_destino}: {e}")
            return None
        
    # Inicia a thread para escutar os comandos sem interromper as ações do peer
    def escutar(self):
        threading.Thread(target=self.receive.escutar, daemon=True).start()

    def mataSockets(self):
        if hasattr(self, "socket_listen") and self.socket_listen:
            self.socket_listen.close()
        if hasattr(self, "socket_send") and self.socket_send:
            self.socket_send.close()
    
    # Comandos GET e de atualização para alguns atributos do peer
    def attClock(self):
        self.clock += 1
    
    def attClock2(self, newClock):
        self.clock = int(newClock + 1)
        
    def getClock(self):
        return self.clock
    
    def getIP(self):
        return self.ip
    
    def getPorta(self):
        return self.porta
    
    def getIpPorta(self):
        return f"{self.getIP()}:{self.getPorta()}"

    # métodos que encapsulam chamadas de métodos de lógica dos comandos
    def listarPeers(self):
        self.send.listarPeers()

    def obterPeers(self):
        self.send.obterPeers()

    def sair(self):
        self.send.sair()
        
    def buscarArq(self):
        self.send.buscarArq()
        
    def handlePeersList(self, connecSocket):
        self.receive.handlePeersList(connecSocket)
        
    def handleLSList(self, connecSocket):
        self.receive.handleLSList(connecSocket)
    
    def exibeArquivosEncontrados(self):
        self.send.exibeArquivosEncontrados()
    
    def sair(self):
        self.send.sair()
        
    def listarArqLoc(self):
        arquivos = os.listdir(self.peerdir)
        arquivos_formatados = []
        for arquivo in arquivos:
            arquivos_formatados.append(os.path.basename(arquivo))


        for arquivo in arquivos_formatados:
            print(arquivo)
            
    def qtdArqLoc(self):
        arquivos = os.listdir(self.peerdir)
        return len(arquivos)
    
    def listaArqTam(self):
        arquivos = os.listdir(self.peerdir)
        arquivos_formatados = []

        for arquivo in arquivos:
            caminho = os.path.join(self.peerdir, arquivo)
            tamanho = os.path.getsize(caminho)
            arquivos_formatados.append(f"{arquivo},{tamanho}")

        return " ".join(arquivos_formatados)
    
    def adicionar_novo_arq_encontrado(self, nome, tam, peer):
        for arq in self.arqEncontrados:
            if arq["nome"] == nome and arq["tamanho"] == tam and arq["peer"] == peer:
                return
        
        self.arqEncontrados.append({
        "nome": nome,
        "tamanho": tam,
        "peer": peer
    })
        
        #for arquivoTam in arquivos_formatados:
        #    print(arquivoTam)


    
