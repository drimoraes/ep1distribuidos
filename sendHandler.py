import socket
import threading
import sys
import os
from message import Message


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
                    destinatario = self.peer.arqEncontrados[escolha]['peer']  
                    self.peer.attClock()
                    clock = self.peer.getClock()
                    print (f"Atualizando relógio para {clock}")
                    connection_socket = Message.mensagemDL(self.peer, destinatario, clock, self.peer.arqEncontrados[escolha]['nome'])
                    if connection_socket: 
                        self.peer.handleFILE(connection_socket)
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Opção inválida! Por favor, escolha um número.")



                

    