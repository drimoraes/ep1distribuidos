import threading

class HandlerReceive:
    def __init__(self, peer):
        self.peer = peer

    def escutar(self):
        self.peer.socket.listen(4)
        print("Escutando por conexões...")

        while True:
            conn, addr = self.peer.socket.accept()
            print(f"Conexão recebida de {addr}")
            threading.Thread(target=self.tratarReq, args=(conn, addr), daemon=True).start()

    def tratarReq(self, conn, addr):
        # Identifica o código da mensagem
        data = conn.recv(1024)

        try:
            data_str = data.decode('utf-8')  # Decodifica os dados para string
            origem, clock, tipo, argumentos = self.processarMensagem(data_str)

            # Executa diferentes lógicas dependendo do TIPO
            if tipo == "HELLO":
                self.handleHello(origem, clock)
            elif tipo == "GET_PEERS":
                self.handleGetPeers(origem, clock)
            elif tipo == "LIST_FILES":
                self.handleListFiles(origem, clock)
            else:
                print(f"Tipo {tipo} desconhecido.")

        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    def handleHello(self, origem, clock):
        print(f"Mensagem recebida: {origem}, {clock}, HELLO")
        self.peer.attClock()
        print(f"Atualizando relógio para {self.peer.getClock()}")
        # Adiciona quem mandou na lista de status online

    def handleGetPeers(self, origem, clock):
        print(f"Mensagem recebida: {origem}, {clock}, GET_PEERS")
        # Lógica para lidar com GET_PEERS

    def handleListFiles(self, origem, clock):
        print(f"Mensagem recebida: {origem}, {clock}, LIST_FILES")
        # Lógica para lidar com LIST_FILES

    def processarMensagem(self, data_str):
            # fazer
        
       #return origem, clock, tipo, argumentos