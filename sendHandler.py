import socket
import threading
import sys
import os
from message import Message
import time


class HandlerSend:
    def __init__(self, peer):
        self.peer = peer

    def listarPeers(self):
        print("[0] voltar para o menu anterior")
        self.peer.peerslist_handler.listar_peers()
        escolha = input("> ")
        if escolha == "0":
            print("Voltando para o menu...")
        else:
            try:
                escolha = int(escolha) - 1 

                lista_peers = list(self.peer.peerslist["OFFLINE"].keys()) + list(self.peer.peerslist["ONLINE"].keys())

                if 0 <= escolha < len(lista_peers):
                    destinatario = lista_peers[escolha]  
                    self.peer.attClock()
                    clock = self.peer.getClock()
                    print (f"Atualizando relógio para {clock}")
                    Message.mensagemHello(self.peer, destinatario, clock)
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Opção inválida! Por favor, escolha um número.")
                
    def obterPeers(self):
        enviados = []  # Foi necessário adicionar ess estrutura auxiliar para não enviar a mensagem repetidas vezes
        for status in ["OFFLINE", "ONLINE"]:
            for peerDest in list(self.peer.peerslist[status]):
                if peerDest in enviados:
                    continue

                self.peer.attClock()
                clock = self.peer.getClock()
                print(f"Atualizando relógio para {clock}")

                connection_socket = Message.mensagemGetPeers(self.peer, peerDest, clock)
                if connection_socket:  
                    self.peer.handlePeersList(connection_socket)

                enviados.append(peerDest)
                
    def enviaDL(self, index):
        inicio = time.time()
        if not self.peer.arqEncontrados:
            print("Nenhum arquivo encontrado. Por favor, busque arquivos primeiro.")
            return

        arquivos = list(self.peer.arqEncontrados.items())
        nome, tamanho = arquivos[index][0]
        peers = arquivos[index][1]
        chunk = self.peer.chunk
        indexChunk = 0
        totalChunks = int(tamanho) // chunk + (1 if int(tamanho) % chunk > 0 else 0)
        chunkList = [None] * totalChunks
        while indexChunk < totalChunks:
            for peerDest in peers:
                if indexChunk >= totalChunks:
                    break
                self.peer.attClock()
                clock = self.peer.getClock()
                print(f"Atualizando relógio para {clock}")
                connection_socket = Message.mensagemDL(self.peer, peerDest, clock, nome, chunk, indexChunk)
                if connection_socket: 
                    chunkList[indexChunk] = self.peer.handleChunk(connection_socket)
                indexChunk += 1
        final = time.time()
        tempo = final - inicio
        self.peer.atualizaStats(len(peers), tamanho, tempo)
        self.peer.handleFILE(nome, chunkList)
                
    def buscarArq(self):
        enviados = [] 
        for status in ["ONLINE"]:
            for peerDest in self.peer.peerslist[status]:
                if peerDest in enviados:
                    continue

                self.peer.attClock()
                clock = self.peer.getClock()
                print(f"Atualizando relógio para {clock}")

                connection_socket = Message.mensagemBuscaArq(self.peer, peerDest, clock)
                if connection_socket: 
                    self.peer.handleLSList(connection_socket)

                enviados.append(peerDest)
                
            self.exibeArquivosEncontrados()

    def sair(self):
        print('Saindo...')
        self.peer.attClock()
        clock = self.peer.getClock()
        for destinatario in self.peer.peerslist["ONLINE"]: 
            print (f"=> Atualizando relógio para {clock}")
            Message.mensagemBye(self.peer, destinatario, clock)
        print("Finalizando execução...")
        self.peer.mataSockets()
        sys.exit(0) 
        
    def exibeArquivosEncontrados(self):

        print("Arquivos encontrados na rede:")
        print("Nome | Tamanho | Peers")
        print("[ 0] <Cancelar> | |")

        index = 1
        for (nome, tamanho), peers in self.peer.arqEncontrados.items():
            peers_str = ', '.join(peers)
            print(f"[ {index}] {nome} | {tamanho} | {peers_str}")
            index += 1


        escolha = input("> ")
        if escolha == "0":
            print("Voltando para o menu...")
        else:
            try:
                escolha = int(escolha) - 1 
                if 0 <= escolha < len(self.peer.arqEncontrados):
                    self.enviaDL(escolha)
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Opção inválida! Por favor, escolha um número.")



                

    