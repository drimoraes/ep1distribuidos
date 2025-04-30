import socket, pickle
import sys
import pathlib
import os
import threading
from peer import Peer

# verifica parâmetros
if len(sys.argv) < 3:
    print("Por favor, insira todos os parâmetros necessários: eachare.py <IP:PORT> <arquivo_peers> <diretório>")
    sys.exit(1)


endereco = sys.argv[1]
arquivo = sys.argv[2]
dir = sys.argv[3]

# inicializa o peer
peer = Peer(endereco, arquivo, dir)

# loop principal do sistema
while True:
    print("Escolha um comando: \n [1] Listar peers \n [2] Obter peers \n [3] Listar arquivos locais \n [4] Buscar arquivos \n [5] Exibir estatisticas \n [6] Alterar tamanho de chunk \n [9] Sair")
    escolha = input("> ")
    escolha = int(escolha)
    if escolha == 1:
        peer.listarPeers()
    if escolha == 2:
        peer.obterPeers()
    if escolha == 3:
        peer.listarArqLoc()
    if escolha == 4:
        peer.buscarArq()
    if escolha == 9:
        peer.sair()


