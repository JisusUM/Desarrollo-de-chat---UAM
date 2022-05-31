import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 
# Puede usar cualquier puerto entre 0 y 65535
LISTENER_LIMIT = 10
active_clients = [] 
# Lista de todos los usuarios actualmente conectados


# Función para escuchar los próximos mensajes de un cliente
def listen_for_messages(client, username):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"El mensaje enviado desde el cliente {username} Esta vacía ")


# Función para enviar mensaje a un solo cliente
def send_message_to_client(client, message):

    client.sendall(message.encode())

# Función para enviar cualquier mensaje nuevo a todos los clientes que
# están actualmente conectados a este servidor
def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

#Funcion para manejar cliente
def client_handler(client):
    
    # El servidor escuchará el mensaje del cliente que
    # Contener el nombre de usuario
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "Cinf~" + f"{username} añadido al chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function
def main():

# Creando el objeto de clase de socket
     #AF_INET: vamos a usar direcciones IPv4
     # SOCK_STREAM: estamos usando paquetes TCP para la comunicación
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creando un bloque try catch
    try:
        # Proporcione al servidor una dirección en forma de
        # host IP y puerto
        server.bind((HOST, PORT))
        print(f"Ejecutando el servidor en {HOST} {PORT}")
    except:
        print(f"Incapaz de enlazar a la host {HOST} y porto {PORT}")

    # Establecer límite de servidor
    server.listen(LISTENER_LIMIT)

    # Este bucle while seguirá escuchando las conexiones de los clientes
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()