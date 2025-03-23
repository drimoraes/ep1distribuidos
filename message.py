class Message:
    def __init__(self, remetente, destinatario, tipo, clock):
        self.remetente = remetente
        self.destinatario = destinatario
        self.tipo = tipo
        self.clock = clock

    @staticmethod
    def criarHello(remetente, destinatario, clock):
        return Message(remetente, destinatario, "HELLO", clock)

    def gerarMensagem(self):
        return f"HELLO {self.remetente} {self.destinatario} {self.clock}"
