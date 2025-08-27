import socket, select

HOST = "127.0.0.1"
PORT = 9999

# create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)

socket_list = [server]  # track all sockets
clients = {}  # map socket -> address

print(f"[C2] Listening on {HOST}:{PORT}")

while True:
    read_sockets, _, _ = select.select(socket_list, [], [])
    
    for notified_socket in read_sockets:
        if notified_socket == server:
            # New connection
            client_socket, client_address = server.accept()
            socket_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"[C2] Connection from {client_address} established!")
        else:
            try:
                # Message from a client
                message = notified_socket.recv(1024)
                if not message:
                    # Connection closed
                    print(f"[C2] Bot {clients[notified_socket]} disconnected")
                    socket_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                print(f"[{clients[notified_socket]}] {message.decode()}")
            except:
                socket_list.remove(notified_socket)
                del clients[notified_socket]

    # Send commands to all connected bots
    try:
        cmd = input()
        for client_socket in clients:
            client_socket.send(cmd.encode())
    except EOFError:
        break

server.close()

