
# a biblioteca socket sera usada para conseguir enviar dados atraves da rede
import socket
#ermitem que múltiplas execuções ocorram no mesmo ambiente do aplicativo com
# um grande grau de independência uma da outra
import threading

#o host vai identificar o computador na internet, e port o numero de porta tcp assciado ao protocolo
HOST = input("Host: ")
PORT = int(input("Port: "))

#foi criado o tipo de transmissao que é sock stream que é basicamente tcp
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#servidor de protocolo DNS
server.bind((HOST,PORT))
#vai  iniciar o servidor para ouvir a conexão criptografada.
server.listen()
print(f'Server is Up and Listening on {HOST}:{PORT}')


#lista vazia para guardar os ips dos clientes e ouvir pq cada thread vai ser um cliente , sendo processado
#de maneira separada
clients = []
#lista vazia para guardar os nomes de usuario, para user ao nomes ao inves de ip para identificar cada um
usernames = []


#metodo de broadcast para enviar mensagem para todos os usuarios, como por ex, determinado usuarios entrou no chat
def globalMessage(message):
    for client in clients:
        client.send(message)

def handleMessages(client):
    while True:
        #try except para finalizar a conexao quando alguem sai, se nao o servidor ficaria esperando eternamente a msg
        try:
            receiveMessageFromClient = client.recv(2048).decode('ascii')
            globalMessage(f'{usernames[clients.index(client)]} :{receiveMessageFromClient}'.encode('ascii'))
        except:
            clientLeaved = clients.index(client)
            client.close()
            clients.remove(clients[clientLeaved])
            clientLeavedUsername = usernames[clientLeaved]
            print(f'{clientLeavedUsername} has left the chat...')
            globalMessage(f'{clientLeavedUsername} has left us...'.encode('ascii'))
            usernames.remove(clientLeavedUsername)

#essa funçao  que vai pegar o client que ele se conectar ao servidor, vai mandar a mensagem que esta conectado
#e vai adicionar o cliente na lista
def initialConnection():
    while True:
        try:
            client, address = server.accept() #---faz com o que servidor aceite conexoes
            print(f"New Connetion: {str(address)}")
            #como client e username estao com mesmo indice, podemos saber que determinado endereço e de tal username
            clients.append(client)
            #quando envia mensagem decode e quando recebe , decode
            client.send('getUser'.encode('ascii'))   #ascii linguagem padrao para troca de informaçoes, encode mapeia caracteres
            # ----- vai mostrar de qual cliente vai ser recebido a mensagem e o decode vai decodificar a string
            username = client.recv(2048).decode('ascii')

            usernames.append(username) #--------------vai adicionar no username na lista vazia
            globalMessage(f'{username} just joined the chat!'.encode('ascii'))
            #usaremos varias threads para permirtir que multplas execuçoes ocorram no mesmo ambiente de maneira
            #independente
            user_thread = threading.Thread(target=handleMessages,args=(client,)) #-
            user_thread.start()
        except:
            pass

initialConnection()