import re

class Message:

    @staticmethod
    def mensagemHello(remetente, destinatario, clock):
        print(f'Encaminhando mensagem "{remetente.getIpPorta()} {clock} HELLO" para {destinatario}')
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
            
    @staticmethod
    def mensagemGetPeers(remetente, destinatario, clock):
        print(f'Encaminhando mensagem "{remetente.getIpPorta()} {clock} GET_PEERS" para {destinatario}')
        socket_envio = remetente.criar_socket_envio(destinatario)  # Tenta conectar ao peer destino
        #if socket_envio:
        mensagem = f"{remetente.getIpPorta()} {clock} GET_PEERS"
        try:
            socket_envio.send(mensagem.encode())  # Envia a mensagem codificada
            socket_envio.listen(1)
            conn, addr = socket_envio.accept()
            data = conn.recv(1024)
            data_str = data.decode('utf-8')  # Decodifica os dados para string
            origem, clock, tipo, argumentos = Message.processarMensagem(data_str)
            
                
                #if remetente.buscar_peerIP(destinatario):
                #   remetente.atualizar_status_peer(destinatario, "ONLINE")
                #else:
                #   remetente.adicionar_novo_peer(destinatario)

        except Exception as e:
            print(f"Erro ao enviar mensagem para {destinatario}: {e}")
            remetente.atualizar_status_peer(destinatario, "OFFLINE")
        finally:
            socket_envio.close()  # Fecha o socket após o envio
            
    @staticmethod
    def mensagemPeerList(remetente, destinatario, clock, conn):
        print(f'Encaminhando mensagem "{remetente.getIpPorta()} {clock} PEER_LIST" para {destinatario}')
    
        mensagem = f"{remetente.getIpPorta()} {clock} PEER_LIST {remetente.tam_lista() - 1} {remetente.lista_peersStatus(remetente.getIpPorta())}"
    
        try:
            conn.sendall(mensagem.encode())  # Usar `conn`, não criar um novo socket
        except Exception as e:
            print(f"Erro ao enviar mensagem para {destinatario}: {e}")
            remetente.atualizar_status_peer(destinatario, "OFFLINE")
        finally:
            conn.close() 
    
    @staticmethod        
    def processarMensagem(data_str):
        match = re.match(r"(\S+)\s+(\S+)\s+(\S+)\s*(.*)", data_str)

        if match:
            origem = match.group(1)
            clock = match.group(2)
            tipo = match.group(3)
            argumentos = match.group(4).split() if match.group(4) else []  # Se não houver argumentos, retorna lista vazia
            
            return origem, clock, tipo, argumentos
        else:
            # Se a correspondência falhar, retornamos None para os valores
            print("Erro: formato de mensagem inválido.")
            return None, None, None, None
