#This file contains server source code
#Authors: Kingsley Besidonne and Molife Chaplain
#Group number: 33
import socket
import sys
import ipaddress


#dictionary for storing registered nodes and their status

#dictionary for storing nodes in dht


#register function for registering users
def register(Data):
    return "SUCCESS"

#setup function for constructing the dht
def setUp(Data):
    return "SUCCESS"

#dht complete function to check if dht requirements are satisfied
def dhtComplete(Data):
    return "SUCCESS"

#query function for retriving information from dht
def query():
    return "SUCCESS"

#controller function for processing client commands
def controller(data):
    DataArr = data.split(" ")
    command = DataArr.pop(0)
    
    if command == 'register':
        #calls the register function
        return register(DataArr)

    elif command == 'setup-dht':
        #calls the setUp function
        return setUp(DataArr)
        
    elif command == 'dht-complete':
        #calls the dhtComplete function
        return dhtComplete(DataArr)
        
    elif command == 'query-dht':
        #calls the query function
        return query(DataArr)
    
    else:
        return "Command is not valid"



#Class nodes for client node objects
class node:
    def __init__(self, username, ip_address, port):
        self.username = username
        self.ip_address = ip_address
        self.port = port
        #create local hash table for storing information

    #function returns the node username
    def getUsername(self):
        return self.username
    
    #function returns the node ipaddress
    def getIpAddress(self):
        return self.ip_address
    
    #function returns the node port
    def getPort(self):
        return self.port

    #create hash function
    #define function for inserting into hash table
    #define function for getting information


#main function for our code
def main(argv):
    #check if our commandline input parameters are of correct length
    if(len(sys.argv) != 2):
        print("Error: parameter length not correct")
        return 0

    #listening port of server
    port = int(sys.argv[1])

    #local address for server
    #hostAddr = str(ipaddress.IPv4Address('127.0.0.1'))
    host = '127.0.0.1'
    

    #create socket for sending and recieving datagrams
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #Bind the local address and port
        sock.bind((host,port))
        #listen and accept
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                message = controller(data.decode())
                if not data:
                    break
                conn.sendall(str.encode(message))

if __name__ == '__main__' :
    main(sys.argv)

    

    
    
    
    
