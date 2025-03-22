import sys
import socket as s
import select as sel

HOST = '0.0.0.0'
PORT = 4444
SOCKET_LIST = []
RECEIVE_BUFF = 4096

def chat_server():
    server_socket = s.socket(s.AF_INET , s.SOCK_STREAM)
    server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SOCKET_LIST.append(server_socket)
    print(f"CHAT SERVER STARTED LISTENING ON PORT {PORT}")

    while True:
        ready_read, _, _ = sel.select(SOCKET_LIST, [], [], 0)

        for sock in ready_read:
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                SOCKET_LIST.append(client_socket)
                print(f"Client {addr} connected.")
                broadcast(server_socket, client_socket, f"{addr} joined the chat.\n")
            else:
                try:
                    data = sock.recv(RECEIVE_BUFF)
                    if data:
                        message = f"[{sock.getpeername()}] {data.decode()}"
                        print(message.strip())
                        broadcast(server_socket, sock, message)
                    else:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                            broadcast(server_socket, sock, f"{sock.getpeername()} has left the chat.\n")
                except Exception as e:
                    print(f"Error: {e}")
                    continue

def broadcast(server_socket, sender_socket, message):
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sender_socket:
            try:
                socket.send(message.encode())
            except:
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == "__main__":
    chat_server()
