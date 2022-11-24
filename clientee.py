# a biblioteca socket sera usada para conseguir enviar dados atraves da rede
import socket
#permitem que múltiplas execuções ocorram no mesmo ambiente do aplicativo com um
# grande grau de independência uma da outr
import threading

ServerIP = input("Server IP: ")
PORT = int(input("Port: "))
#foi criado o tipo de transmissao que é sock stream que é basicamente tcp
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#o try abaixo foi criado para caso o cliente erre o ip , nao feche a aplicaçao
#e sim exiba para ele a mensagem de erro para que corriga
try:
    nome = []
    username = input('Enter a username: ')
    for letra in username:
        nome.append(letra)
    while(nome[0] == ' ') or (nome[0] == ''):
        nome.clear()
        username = input('Enter a username: ')
        for letra in username:
            nome.append(letra)
    client.connect((ServerIP,PORT))
    print(f'Connected Successfully to {ServerIP}:{PORT}')
except:
    print(f'ERROR: Please review your input: {ServerIP}:{PORT}')
#esse metodo, para o cliente receber as mensagens de outros usuarios, e tbm a respostas do servidor
def receiveMessage():
    while True:
        try:
            message = client.recv(2048).decode('ascii')
            if message=='getUser': #---mensagem do servidor
                client.send(username.encode('ascii'))
            else:
                print(message)#---print as menasgens dos outros usuarios
        except:
            print('ERROR: Check your connection or server might be offline')

def sendMessage(): ####cada vez que dou um input , encoda a mensagem e envia para o servidor
    while True:
        client.send(input().encode('ascii'))


#essa thread vai receber mensagens
thread1 = threading.Thread(target=receiveMessage,args=())
#essa thread vai enviar mensagens
thread2 = threading.Thread(target=sendMessage,args=())
#nao podemos inverter a ordem das threads pq eh necessario primeiro receber a resposta do servido r
#para entao poder enviar

thread1.start()
thread2.start()