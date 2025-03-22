class Message:
    def __init__(self, remetente, destinatario, tipo, clock):
        self.remetente = remetente
        self.destinatario = destinatario
        self.tipo = tipo
        self.clock = clock

    @staticmethod
    def criarHello(remetente, destinatario, clock):
        """Cria uma mensagem do tipo HELLO."""
        return Message(remetente, destinatario, "HELLO", clock)

    def gerarMensagem(self):
        """Gera a mensagem em formato de string para envio."""
        return f"HELLO {self.remetente} {self.destinatario} {self.clock}"
