import socket
import threading
import sys
import os
from message import Message

class HandlerSend:
    def _init_(self, peers, clock):
        self.peers = peers
        self.clock = clock

    def listarPeers(self):
        """Exibe a lista de peers conhecidos e seus status."""
        print("Lista de peers:")
        print("[0] Voltar para o menu anterior")
        for idx, (peer, status, peer_clock) in enumerate(self.peers.items()):
            print(f"[{idx + 1}] {peer} {status} (clock: {peer_clock})")

    def enviarMensagemHELLO(self, peer_destino):
        """Envia a mensagem HELLO para o peer escolhido e atualiza o status dele."""
        endereco, porta = peer_destino.split(":")
        
        # Cria a mensagem HELLO usando a classe Message
        mensagem = Message.criarHello(self.peers['local'], peer_destino, self.clock).gerarMensagem()

        try:
            # Tenta conectar usando o socket existente
            self.peer.socket.connect((self.peer.getIp(), self.peer.getPorta()))

            # Verifica se a conexão foi estabelecida (o connect não gera exceção aqui)
            if self.peer.socket.fileno() == -1:
                print(f"Peer de destino offline, vamos mudar o status dele para OFFLINE {peer_destino}")
                self.peer.atualizarStatus(peer_destino, "OFFLINE")
            
            # Envia a mensagem HELLO após verificar a conexão
            self.peer.socket.send(mensagem.encode())  # Envia a mensagem HELLO
            print(f"Encaminhando mensagem \"{mensagem}\" para {peer_destino}")

            # Atualiza o status do peer para ONLINE
            self.peer.atualizarStatus(peer_destino, "ONLINE")

        except (socket.error, ConnectionRefusedError) as e:
            print(f"Erro ao enviar HELLO para {peer_destino}: {e}")
            # Se falhar, atualiza o status do peer para OFFLINE
            self.atualizarStatus(peer_destino, "OFFLINE")

    def atualizarStatus(self, peer_destino, status):
        """Atualiza o status do peer e exibe a mensagem."""
        print(f"Atualizando peer {peer_destino} status {status}")
        
        # Atualiza o status do peer na lista de peers
        if peer_destino in self.peers:
            self.peers[peer_destino] = status
        else:
            self.peers[peer_destino] = status

    def executarComando(self):
        """Método principal para executar os comandos do usuário."""
        while True:
            self.listarPeers()
            escolha = input("> ")

            if escolha == "0":
                print("Voltando para o menu...")
                break  # Volta para o menu principal
            else:
                try:
                    # Pegando o peer escolhido
                    escolha = int(escolha) - 1
                    if 0 <= escolha < len(self.peers):
                        peer_destino = list(self.peers.keys())[escolha]
                        # Envia a mensagem HELLO para o peer selecionado
                        self.enviarMensagemHELLO(peer_destino)
                    else:
                        print("Opção inválida!")
                except ValueError:
                    print("Opção inválida! Por favor, escolha um número.")