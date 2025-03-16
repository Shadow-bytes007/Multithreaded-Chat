import socket as s
import select as sel
HOST = " "
PORT = 4444
SOCKET_LIST=[]

def chat_server():
    server_socket= s.socket(s.AF_INET,s.SOCK_STREAM)  # 1 added address family and  socket mode
    server_socket.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)  # 2 added how to present in session layer and reuse address
    server_socket.bind(HOST,PORT)   # 3 HOST SHOULD BIND WITH PORT 
    server_socket.listen()      # 4 SOCKETS STARTS LISTENING 
    SOCKET_LIST.append(server_socket)   #5 WHEN SERVER SOCKET ISS USED IT GOES AND SITS IN SOCKET_LIST
    print ("CHAT SERVER STARTED LISTNING "+str(PORT))
    while True:
    #waiting th flow for new incoming connections
        ready_read,ready_write,write = sel.select(SOCKET_LIST,[],[],0)
        for sock in ready_read:
            if sock == server_socket : #just for verifying 
                sockfd , addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print ("client "+addr+"connected")
                #TODO: ACCEPT MESSAG AND BROADCAST
            else :
                try:
                    data = sock.recv(RECEIVE_BUFF)
                    if data :
                        #TODO : ACCEPT MESSAGE AND BROADCAST     
                        pass
                    else:
                                   
            
    
    
    