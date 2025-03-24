import socket, pickle
import sys
import pathlib
import os
import threading
from peer import Peer

# criando sockets
if len(sys.argv) < 3:
    print("Uso correto: script.py <IP:PORT> <diretório>", flush=True)
    sys.exit(1)
# chamar o peer

endereco = sys.argv[1]
arquivo = sys.argv[2]
dir = sys.argv[3]

peer = Peer(endereco, arquivo, dir)

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

