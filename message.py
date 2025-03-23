class Message:
    def __init__(self, remetente, destinatario, tipo, clock):
        self.remetente = remetente
        self.destinatario = destinatario
        self.tipo = tipo
        self.clock = clock

    @staticmethod
    def mensagemHello(remetente, destinatario, clock):
        print(f"Encaminhando mensagem '{remetente.getIpPorta()} {clock} HELLO' para {destinatario}")
        socket_envio = remetente.criar_socket_envio(destinatario)  # Tenta conectar ao peer destino
        if socket_envio:
            mensagem = f"{remetente.getIpPorta()} {clock} HELLO"
            try:
                socket_envio.send(mensagem.encode())  # Envia a mensagem codificada
                
                # Se o envio for bem-sucedido, atualizamos o status do peer
                remetente.atualizar_status_peer(destinatario, "ONLINE")

            except Exception as e:
                print(f"Erro ao enviar mensagem para {destinatario}: {e}")
            finally:
                socket_envio.close()  # Fecha o socket após o envio
        else:
            remetente.atualizar_status_peer(destinatario, "OFFLINE")
