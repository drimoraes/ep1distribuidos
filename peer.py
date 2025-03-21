import socket
import sys
import os

# Verificando argumentos
if len(sys.argv) < 3:
    print("Uso correto: script.py <IP:PORT> <diretório>", flush=True)
    sys.exit(1)

# Criando socket
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtendo IP e PORT
IP, PORT = sys.argv[1].split(":")
PORT = int(PORT)  # Convertendo PORT para inteiro

print(f"IP: {IP}, PORT: {PORT}", flush=True)  # Verificando IP e PORT

try:
    peer_socket.bind((IP, PORT))
    print("Socket OK", flush=True)
except Exception as e:
    print(f"Erro ao vincular o socket: {e}", flush=True)
    sys.exit(1)

# Verificando diretório
dir = sys.argv[2]
if not (os.path.isdir(dir) and os.access(dir, os.R_OK)):
    print("Erro: O diretório não existe ou não tem permissão de leitura.", flush=True)
    sys.exit(1)
print("Verificação OK", flush=True)

# Exibindo opções
print("Escolha um comando: \n [1] Listar peers \n [2] Obter peers \n [3] Listar arquivos locais \n [4] Buscar arquivos \n [5] Exibir estatísticas \n [6] Alterar tamanho de chunk \n [9] Sair", flush=True)

# Escutando conexões
peer_socket.listen(5)  # Ou outro número que achar adequado
print("Escutando conexões...", flush=True)