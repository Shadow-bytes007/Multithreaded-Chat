import sys
import socket as s
import select as sel
HOST = ""
PORT = 4444
SOCKET_LIST=[]
RECEIVE_BUFF = 4096

def chat_server():
    server_socket= s.socket(s.AF_INET,s.SOCK_STREAM)  # 1 added address family and  socket mode
    server_socket.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)  # 2 added how to present in session layer and reuse address
    server_socket.bind((HOST,PORT))   # 3 HOST SHOULD BIND WITH PORT 
    server_socket.listen()      # 4 SOCKETS STARTS LISTENING 
    SOCKET_LIST.append(server_socket)   #5 WHEN SERVER SOCKET ISS USED IT GOES AND SITS IN SOCKET_LIST
    print ("CHAT SERVER STARTED LISTNING "+str(PORT))
    while True:
        
    #waiting th flow for new incoming connections
        ready_read,ready_write,error = sel.select(SOCKET_LIST,[],[],0)
        for sock in ready_read:
            if sock == server_socket : #just for verifying 
                client_socket , addr = server_socket.accept()
                SOCKET_LIST.append(client_socket)
                print ("client {} connected.\n".format(addr))
                broadcast(server_socket,client_socket,"{} entered our chatting root \n".format(addr))
           
            else:
                try:
                    data = sock.recv(RECEIVE_BUFF)
                    if data :
                        broadcast(server_socket,client_socket,"[{}] {}".format(sock.getpeername(), data))   
                        pass
                    else:
                        #The socket must have been broken, remove from list and broadcast a message
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                            #TODO : BRODCAST THAT SOMEONE DISCONNECTED
                except:
                    #TODO : BROADCAST  THAT SOMEONE HAS DISCONNECTED
                    continue
                #TODO : PLAN EXIT STRATEGY   
             #   server_socket.close()
                
    # message should be broadcasted other than the person who sent message, the server(even considered server as entity)                                   
def broadcast(server_socket,client_socket,message):
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != client_socket:
            try:
                socket.send(message.encode())
                socket.flush()
            except:
                # it shoukld be a broken connection
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)                 
if __name__ == "__main__":
    sys.exit(chat_server())  
   
    