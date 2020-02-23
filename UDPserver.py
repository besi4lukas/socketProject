#This file contains server source code
#Authors: Kingsley Besidonne and Molife Chaplain
#Group number: 33
import socket
import sys
import ipaddress


#dictionary for storing registered nodes and their status
reg_nodes = {}

#dictionary for storing nodes in dht
dht_node = {}

#list for unavailable ports
used_ports = []


#register function for registering users
def register(Data):
    keys = reg_nodes.keys()
    username = Data[0]
    ip = Data[1]
    port = Data[2]
    status = "Free"
    
    #check if port and username is unique
    if(username in keys):
        return "FAILURE: username is not unique"
    elif(port in used_ports):
        return "FAILURE: port is not unique"
        
    #create node object with data
    nodeObj = node(username,ip,port,status)
    
    #add node to registered nodes dictionary
    reg_nodes[username] = nodeObj
    
    #add port to used ports
    used_ports.append(port)
    
    return "SUCCESS"

#setup function for constructing the dht
def setUp(Data):
    return "SUCCESS"

#dht complete function to check if dht requirements are satisfied
def dhtComplete(Data):
    return "SUCCESS"

#query function for retriving information from dht
def query(Data):
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
    def __init__(self, username, ip_address, port, status):
        self.username = username
        self.ip_address = ip_address
        self.port = port
        self.status = status
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

    #function return the status of the node
    def getStatus(self):
        return self.status
    
    #function changes the status of the node
    def setStatus(self, newStatus):
        self.status = newStatus

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
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serverSocket:
        #Bind the local address and port
        serverSocket.bind((host,port))
        print("Server is ready to receive...")
        while True:
            data, clientAddr = serverSocket.recvfrom(2048)
            message = controller(data.decode())
            if not data:
                break
            serverSocket.sendto(str.encode(message))

if __name__ == '__main__' :
    main(sys.argv)

    

    
    
    
    
