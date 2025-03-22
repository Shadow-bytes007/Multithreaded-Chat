import sys
import socket
import select as sel

def chat_client():
    if len(sys.argv)<3:
        print("Usage: python3 {} <hostname> <port>".format(sys.argv[0]))
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    # Try connecting to the server
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"Cannot reach {host}:{port} ... ({e})")
        sys.exit(1)

    print("Connected to remote host. You can start sending messages...")

    SOCKET_LIST = [s]
    sys.stdout.write("> ")
    sys.stdout.flush()

    while True:
        read_ready, read_write, error = sel.select(SOCKET_LIST, [], [])
        
        for sock in read_ready: 
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print("\nDisconnected from server.")
                    sys.exit()
                else:
                    sys.stdout.write(data.decode())
                    sys.stdout.write("\n> ")
                    sys.stdout.flush()
            else:
                msg = input("YOU > ")
                s.send(msg.encode())
                sys.stdout.write("> ")
                sys.stdout.flush()

if __name__ == "__main__":
    chat_client()
