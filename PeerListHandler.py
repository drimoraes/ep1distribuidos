import sys

class PeerListHandler:

    def __init__(self, list):
        self.peerslist = list

    def carrega_peers(self, arquivo):
        try:
            with open(arquivo, "r") as file:
                for linha in file:
                    endereco = linha.strip()
                    if endereco:
                        self.peerslist["OFFLINE"].append(endereco)
                        print(f"Adicionando novo peer {endereco} status OFFLINE")

        except FileNotFoundError:
            print(f"Erro: O arquivo {arquivo} não foi encontrado.")
            sys.exit(1)

    def atualizar_status(self, peer, novo_status):
        if novo_status not in ["ONLINE", "OFFLINE"]:
            print("Erro: Status inválido. Use 'ONLINE' ou 'OFFLINE'.")
            return
        
        if novo_status == "OFFLINE":
            status_antigo = "ONLINE"
        else:
            status_antigo = "OFFLINE"

        if peer in self.peerslist[status_antigo]: 
            self.peerslist[status_antigo].remove(peer)
            self.peerslist[novo_status].append(peer) 
            print(f"Atualizando peer {peer} status {novo_status}")
        else:
            print(f"O peer {peer} já está {novo_status}")

    # Adiciona um novo peer na lista com status desejado.
    def adicionar_peer(self, peer, status):
        if peer in self.peerslist["ONLINE"] or peer in self.peerslist["OFFLINE"]:
            print(f"O peer {peer} já existe na lista.")
            return
        self.peerslist[status].append(peer) 
        print(f"Adicionando novo peer {peer} status {status}")

    
    def busca_peerIP(self, dest):
        for status in ["ONLINE", "OFFLINE"]:
            if dest in self.peerslist[status]:   
                return True  
        return False 
 
    def listar_peers(self):
        index = 1 
        for status in ["OFFLINE", "ONLINE"]:  
            for peer in self.peerslist[status]:  
                print(f"[{index}] {peer} {status}")  
                index += 1 

    # Retorna lista de peers no formato exigido por PEER LIST
    def lista_peersStatus(self, excluir_peer):
        peers_formatados = []

        for status in ["OFFLINE", "ONLINE"]:
            for peer in self.peerslist[status]:
                if peer != excluir_peer:  # Exclui o peer que enviou a mensagem GET PEERS
                    peers_formatados.append(f"{peer}:{status}:0")
        return " ".join(peers_formatados)
    
    # Retorna o número total de peers (ONLINE + OFFLINE).
    def tamanho_lista(self):
        return len(self.peerslist["ONLINE"]) + len(self.peerslist["OFFLINE"])
                