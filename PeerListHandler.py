class PeerListHandler:
    """Gerencia a lista de peers (ONLINE e OFFLINE)."""

    def __init__(self):
        self.peerslist = {"ONLINE": [], "OFFLINE": []}

    def carrega_peers(self, arquivo="peerlist.txt"):
        """Lê o arquivo e adiciona os peers como OFFLINE."""
        try:
            with open(arquivo, "r") as file:
                for linha in file:
                    endereco = linha.strip()
                    if endereco:
                        self.peerslist["OFFLINE"].append(endereco)
                        print(f"Adicionando novo peer {endereco} status OFFLINE")

            print("\nEstrutura da peerslist:", self.peerslist)

        except FileNotFoundError:
            print(f"Erro: O arquivo {arquivo} não foi encontrado.")

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

    def adicionar_peer(self, peer):
        """Adiciona um novo peer na lista com status ONLINE."""
        if peer in self.peerslist["ONLINE"] or peer in self.peerslist["OFFLINE"]:
            print(f"Erro: O peer {peer} já existe na lista.")
            return

        self.peerslist["ONLINE"].append(peer)  # Adiciona o peer como ONLINE
        print(f"Adicionando novo peer {peer} status ONLINE")

    def busca_peer(self, peer):
        """Busca um peer específico (IP:PORTA) e retorna o IP e a porta separadamente."""
        for status in ["ONLINE", "OFFLINE"]:
            if peer in self.peerslist[status]:  
                ip, porta = peer.split(":")  
                return ip, porta  
        return ("", "")  # ✅ Retorna strings vazias em vez de None
