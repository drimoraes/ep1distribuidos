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
                escolha = int(escolha) - 1  # Ajusta o índice para começar do 0
                # Criamos uma lista ordenada contendo apenas os peers (chaves IP:PORTA)
                lista_peers = list(self.peer.peerslist_handler.peerslist["OFFLINE"] + self.peer.peerslist_handler.peerslist["ONLINE"] )

                if 0 <= escolha < len(lista_peers):
                    destinatario = lista_peers[escolha]  # Obtém o IP:PORTA correspondente
                    self.peer.attClock()
                    clock = self.peer.getClock()
                    print (f"Atualizando relógio para: {clock}")
                    Message.mensagemHello(self.peer, destinatario, clock)
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Opção inválida! Por favor, escolha um número.")


 

        