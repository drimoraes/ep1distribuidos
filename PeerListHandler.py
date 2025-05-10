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
                        self.peerslist["OFFLINE"][endereco] = 0  # Agora adiciona com clock 0
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
            clock = self.peerslist[status_antigo].pop(peer)  # Pega o clock e remove do antigo
            self.peerslist[novo_status][peer] = clock        # Adiciona no novo status com mesmo clock
            print(f"Atualizando peer {peer} status {novo_status}")
        #else:
           #print(f"O peer {peer} já está {novo_status}")

    def adicionar_peer(self, peer, status, clock=0):
        if peer in self.peerslist["ONLINE"] or peer in self.peerslist["OFFLINE"]:
            print(f"O peer {peer} já existe na lista.")
            return
        self.peerslist[status][peer] = clock  # Adiciona com clock inicial
        print(f"Adicionando novo peer {peer} status {status}")

    def adicionar_peer2(self, peer, status, clock=0):
        # Peer já está na lista? Então verifica em qual status
        for s in ["ONLINE", "OFFLINE"]:
            if peer in self.peerslist[s]:
                clock_atual = self.peerslist[s][peer]
                if clock > clock_atual:
                    self.peerslist[s][peer] = clock
                return

        # Se não está em nenhuma lista, adiciona com clock (0 ou passado)
        self.peerslist[status][peer] = clock
        print(f"Adicionando novo peer {peer} : {status} : {clock}")


    def busca_peerIP(self, dest):
        for status in ["ONLINE", "OFFLINE"]:
            if dest in self.peerslist[status]:   
                return True  
        return False 
 
    def listar_peers(self):
        index = 1 
        for status in ["OFFLINE", "ONLINE"]:  
            for peer, clock in self.peerslist[status].items():  
                print(f"[{index}] {peer} :{status} :{clock}")  
                index += 1 

    def lista_peersStatus(self, excluir_peer):
        peers_formatados = []
        for status in ["OFFLINE", "ONLINE"]:
            for peer, clock in self.peerslist[status].items():
                if peer != excluir_peer:  
                    peers_formatados.append(f"{peer}:{status}:{clock}")  # Inclui clock certo
        return " ".join(peers_formatados)
    
    def tamanho_lista(self):
        return len(self.peerslist["ONLINE"]) + len(self.peerslist["OFFLINE"])
    
    def returnClock(self, peer_ip_porta):
        for status in ["ONLINE", "OFFLINE"]:
            if peer_ip_porta in self.peerslist[status]:
                return self.peerslist[status][peer_ip_porta]
        print(f"Peer {peer_ip_porta} não encontrado.")
        return None
    
    def atualizarClock(self, peer_ip_porta, novo_clock):
        for status in ["ONLINE", "OFFLINE"]:
            if peer_ip_porta in self.peerslist[status]:
                self.peerslist[status][peer_ip_porta] = novo_clock
                return
        print(f"Peer {peer_ip_porta} não encontrado.")
