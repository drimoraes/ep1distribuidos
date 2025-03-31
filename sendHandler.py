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

                lista_peers = list(self.peer.peerslist["OFFLINE"] + self.peer.peerslist["ONLINE"] )

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
            for peerDest in self.peer.peerslist[status]:
                if peerDest in enviados:
                    continue

                self.peer.attClock()
                clock = self.peer.getClock()
                print(f"Atualizando relógio para {clock}")

                connection_socket = Message.mensagemGetPeers(self.peer, peerDest, clock)
                if connection_socket: 
                    self.peer.handlePeersList(connection_socket)

                enviados.append(peerDest)

    def sair(self):
        print('Saindo...')
        self.peer.attClock()
        clock = self.peer.getClock()
        print (f"=> Atualizando relógio para {clock}")
        for destinatario in self.peer.peerslist["ONLINE"]: 
            Message.mensagemBye(self.peer, destinatario, clock)
        print("Finalizando execução...")
        self.peer.mataSockets()
        sys.exit(0) 
        


                

    