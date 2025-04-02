import re 

class Message:

    @staticmethod
    def mensagemHello(remetente, destinatario, clock):
        print(f'Encaminhando mensagem "{remetente.getIpPorta()} {clock} HELLO" para {destinatario}')
        socket_envio = remetente.criar_socket_envio(destinatario) 
        if socket_envio:
            mensagem = f"{remetente.getIpPorta()} {clock} HELLO"
            try:
                socket_envio.send(mensagem.encode()) 
                
                remetente.atualizar_status_peer(destinatario, "ONLINE")

            except Exception as e:
                print(f"Erro ao enviar mensagem para {destinatario}: {e}")
            finally:
                socket_envio.close() 
        else:
            remetente.atualizar_status_peer(destinatario, "OFFLINE")
    
    def mensagemBye(remetente, destinatario, clock):
        print(f'Encaminhando mensagem "{remetente.getIpPorta()} {clock} BYE" para {destinatario}')
        socket_envio = remetente.criar_socket_envio(destinatario)
        mensagem = f"{remetente.getIpPorta()} {clock} BYE"
        try:
            socket_envio.send(mensagem.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem para {destinatario}: {e}")
        

            
    @staticmethod
    def mensagemGetPeers(remetente, destinatario, clock):
        print(f'Encaminhando mensagem "{remetente.getIpPorta()} {clock} GET_PEERS" para {destinatario}')
        socket_envio = remetente.criar_socket_envio(destinatario) 
        mensagem = f"{remetente.getIpPorta()} {clock} GET_PEERS"
        try:
            socket_envio.send(mensagem.encode())
            return socket_envio
        
        except Exception as e:
            print(f"Erro ao enviar mensagem para {destinatario}: {e}")
            remetente.atualizar_status_peer(destinatario, "OFFLINE")
            

            
    @staticmethod
    def mensagemPeerList(remetente, destinatario, clock, conn):
        if (remetente.buscar_peerIP(destinatario)):
            tam_lista = remetente.tam_lista() - 1
        else:
            tam_lista = remetente.tam_lista()
        print(f'Encaminhando mensagem "{remetente.getIpPorta()} {clock} PEER_LIST {tam_lista} {remetente.lista_peersStatus(destinatario)}" para {destinatario}')
        mensagem = f"{remetente.getIpPorta()} {clock} PEER_LIST {tam_lista} {remetente.lista_peersStatus(destinatario)}"
    
        try:
            conn.sendall(mensagem.encode()) 
        except Exception as e:
            print(f"Erro ao enviar mensagem para {destinatario}: {e}")

        finally:
            conn.close() 

    # trata as mensagens separando e retornando os componentes dela
    @staticmethod        
    def processarMensagem(data_str):
        match = re.match(r"(\S+)\s+(\S+)\s+(\S+)\s*(.*)", data_str)

        if match:
            origem = match.group(1)
            clock = match.group(2)
            tipo = match.group(3)
            argumentos = match.group(4).split() if match.group(4) else []
            
            return origem, clock, tipo, argumentos
        else:
            print("Erro: formato de mensagem inválido.")
            return None, None, None, None
