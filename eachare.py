import socket, pickle
import sys
import pathlib
import os


# criando socket
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP, PORT = sys.argv[1].split(":")
PORT = int(PORT)
peer_socket.bind((IP, PORT))
print("socket ok")
# verificando diretorio
dir = sys.argv[2]
if not (os.path.isdir(dir) and os.access(dir, os.R_OK)):
    sys.exit(1)
    
print("verificação ok")
print("Escolha um comando: \n [1] Listar peers \n [2] Obter peers \n [3] Listar arquivos locais \n [4] Buscar arquivos \n [5] Exibir estatisticas \n [6] Alterar tamanho de chunk \n [9] Sair")
peer_socket.listen(4)