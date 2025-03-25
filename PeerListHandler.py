import sys

class PeerListHandler:
    """Gerencia a lista de peers (ONLINE e OFFLINE)."""

    def __init__(self, list):
        self.peerslist = list

    def carrega_peers(self, arquivo):
        """Lê o arquivo e adiciona os peers como OFFLINE."""
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
        """Atualiza o status de um peer (move entre ONLINE e OFFLINE)."""
        if novo_status not in ["ONLINE", "OFFLINE"]:
            print("Erro: Status inválido. Use 'ONLINE' ou 'OFFLINE'.")
            return
        
        status_antigo = "ONLINE" if novo_status == "OFFLINE" else "OFFLINE"  # Define o status anterior

        if peer in self.peerslist[status_antigo]:  # Se o peer está no status antigo
            self.peerslist[status_antigo].remove(peer)  # Remove do status atual
            self.peerslist[novo_status].append(peer)  # Move para o novo status
            print(f"Atualizando peer {peer} status {novo_status}")
        else:
            print(f"Erro: O peer {peer} não está na lista {status_antigo}, não pode ser movido.")

    def adicionar_peer(self, peer, status):
        """Adiciona um novo peer na lista com status ONLINE."""
        if peer in self.peerslist["ONLINE"] or peer in self.peerslist["OFFLINE"]:
            print(f"Erro: O peer {peer} já existe na lista.")
            return

        self.peerslist[status].append(peer)  # Adiciona o peer como ONLINE
        print(f"Adicionando novo peer {peer} status {status}")

    #def busca_peer(self, peer):
    #    """Busca um peer específico (IP:PORTA) e retorna o IP e a porta separadamente."""
    #    for status in ["ONLINE", "OFFLINE"]:
    #        if peer in self.peerslist[status]:  
    #            ip, porta = peer.split(":")  
    #            return ip, porta  
    #    return ("", "")  # ✅ Retorna strings vazias em vez de None
    
    def busca_peerIP(self, dest):
        """Busca um peer específico (IP:PORTA) e retorna o IP e a porta separadamente."""
        for status in ["ONLINE", "OFFLINE"]:
            if dest in self.peerslist[status]:   
                return True  
        return False 
 
    def listar_peers(self):
        """Lista todos os peers primeiro OFFLINE, depois ONLINE, com um índice numérico."""
        index = 1  # Inicia a numeração em 1
        for status in ["OFFLINE", "ONLINE"]:  # Primeiro OFFLINE, depois ONLINE
            for peer in self.peerslist[status]:  
                print(f"[{index}] {peer} {status}")  
                index += 1  # Incrementa o contador
                
    def lista_peersStatus(self, excluir_peer):
        """Retorna uma string com todos os peers no formato <endereço>:<porta>:<status>:0 separados por espaço, exceto o peer especificado."""
        peers_formatados = []

        for status in ["OFFLINE", "ONLINE"]:
            for peer in self.peerslist[status]:
                if peer != excluir_peer:  # Exclui o peer especificado
                    peers_formatados.append(f"{peer}:{status}:0")
        print(" ".join(peers_formatados))
        return " ".join(peers_formatados)
                
    def tamanho_lista(self):
        """Retorna o número total de peers (ONLINE + OFFLINE)."""
        return len(self.peerslist["ONLINE"]) + len(self.peerslist["OFFLINE"])
                