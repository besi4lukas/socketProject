#This file contains server source code
#Authors: Kingsley Besidonne and Molife Chaplain
#Group number: 33
from socket import *
import sys
import ipaddress
import random
import json


#dictionary for storing registered node objects
reg_nodes = {}

#list for storing nodes in dht
dht_node = []

#list for unavailable ports
used_ports = []

dht_completed = False


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
    
    return {'code': "SUCCESS"}

#setup function for constructing the dht
def setUp(Data):
    ring = Data[0]
    username = Data[1]
    keys = reg_nodes.keys()
    
    #check if user is registered
    if (username not in keys):
        return "FAILURE: not a registered user"
    #check if n is atleast 2
    elif (not (int(ring) >= 2)):
        return "FAILURE: ring size is too small"    
    
    #check if there are atleast n users registered
    elif (not (len(keys) >= int(ring))):
        return "FAILURE: users are too small"
    
    #check if there is exits a dht
    elif (dht_node):
        return "FAILURE: dht already exists"

    else:
        #set the state of username to leader
        dht_node.append(reg_nodes[username])
        dht_node[0].setStatus('Leader')

        #select random n-1 free users and change the state of users to inDHT
        index = random.sample(range(1,len(keys)-1),(ring - 1))
        keys.remove(username)
        for i in index:
            #put users into dht_node list
            tempObj = reg_nodes[keys[i]]
            tempObj.setStatus('InDHT')
            dht_node.append(tempObj)
            keys.pop(i)
        tempList = []
        for obj in dht_node:
            nTuple = (obj.getUsername, obj.getIpAddress, obj.getPort)
            tempList.append(nTuple)

    return {'code': "SUCCESS", 'nodes':tempList}


    

#dht complete function to check if dht requirements are satisfied
def dhtComplete(Data):
    #check if user is registered
    username = Data[0]
    keys = reg_nodes.keys()
    if (username in keys):
        nodeobj = reg_node[username]
        #check if the user is a leader
        if (nodeobj.getStatus() != 'Leader'):
            return "FAILURE"
        
    dht_completed = True
    
    return {'code': "SUCCESS"}


#query function for retriving information from dht
def query(Data):
    #check if user is registered
    if(dht_completed):
        username = Data[0]
        keys = reg_nodes.keys()
        if (username in keys):
            nodeobj = reg_node[username]
            if(nodeobj.getStatus() == 'Free'):
                index = random.randint(1,len(dht_node))
                query_node = dht_node[index]
                node_tuple = (query_node.getUsername,query_node.getIpAddress,query_node.getPort)
            else:
                return  {'code': "FAILURE", 'error': "node is not free"}
        else:
            return {'code': "FAILURE", 'error': "user is not registered"}
    else:
        return {'code': "FAILURE", 'error': "node is not free"}

    return {'code': "SUCCESS"}


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
        self.username = username #username of node
        self.ip_address = ip_address #ipaddress of node
        self.port = port #port of the node
        self.status = status #status of node
 

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
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    #Bind the local address and port
    serverSocket.bind((host,port))
    while True:
        data, clientAddr = serverSocket.recvfrom(2048)
        message = json.dumps(controller(data.decode()))
        if not data:
            break
        serverSocket.sendto(str.encode(message), clientAddr)

if __name__ == '__main__' :
    main(sys.argv)

    

    
    
    
    
