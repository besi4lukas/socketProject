#This file contains server source code
#Authors: Kingsley Besidonne and Molife Chaplain
#Group number: 33
from socket import *
import sys
import ipaddress
import random
import json
from base import dht
dht = dht()


#register function for registering users
def register(Data):
    #Check if the data from user is empty
    if(not(Data)):
        return {"code":"Incomplete command"}

    keys = dht.get_reg_nodes().keys()
    username = Data[0]
    ip = Data[1]
    port = Data[2]
    state = "Free"
    
    #check if port and username is unique
    if(username in keys):
        return {"code":"FAILURE: username is not unique", "node":"empty"}
    elif(len(username) > 15):
        return {"code":"FAILURE: username is too long", "node":"empty"}
    elif(port in dht.get_used_ports()):
        return {"code":"FAILURE: port is not unique", "node":"empty"}
        
    #create node object with data
    nodeObj = node(username,ip,port,state)
    
    #add node to registered nodes dictionary
    dht.add_reg_nodes(username,nodeObj)
    # reg_nodes[username] = nodeObj
    
    #add port to used ports
    dht.add_used_ports(port)
    #used_ports.append(port)
    node_table = {"ip":ip, "port":port}
    
    return {"code":"SUCCESS", "node":node_table}

#setup function for constructing the dht
def setUp(Data):
    
    ring = Data[0]
    username = Data[1]
    keys = dht.get_reg_nodes().keys()
    
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
    elif (dht.get_dht_node()):
        return "FAILURE: dht already exists"

    else:
        #set the state of username to leader
        leaderObj = dht.get_reg_nodes()[username]
        leaderObj.setState("Leader")
        dht.add_dht_node(leaderObj)
        # dht.add_reg_nodes(username,leaderObj)

        #select random n-1 free users and change the state of users to inDHT
        size = int(ring) 
        size_dht = len(dht.get_dht_node())

        if(not(keys)):
            return {"code":"error: no registered nodes"}
        
        for key in keys:
            tempObj = dht.get_reg_nodes()[key]
            if (tempObj.getState() == "Free"):
                tempObj.setState("InDHT")
                dht.add_dht_node(tempObj)
                # dht.add_reg_nodes(tempObj.getUsername(),tempObj)
                size_dht += 1
                if size_dht == size:
                    break
            else:
               dht.add_reg_nodes(tempObj.getUsername(),tempObj) 

        #get the nodes in the DHT and place in a 3-tuple
        node_table = []
        for obj in dht.get_dht_node():
            nTuple = {"username":obj.getUsername(), "ip":obj.getIpAddress(),"port":obj.getPort(),"state":obj.getState(),"ring":ring}
            node_table.append(nTuple)

    return {"code": "SUCCESS", "node":node_table}


    

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
    
##    elif command == 'leave-dht':
##        #calls the query function
##        return query(DataArr)
    
##    elif command == 'dht-rebuilt':
##        #calls the query function
##        return query(DataArr)
    
    elif command == 'deregister':
        #calls the query function
        return query(DataArr)
    
##    elif command == 'teardown-dht':
##        #calls the query function
##        return query(DataArr)
    
##    elif command == 'teardown-complete':
##        #calls the query function
##        return query(DataArr)
    else:
        return {"code":"Command is not valid"}

#Class nodes for client node objects
class node:
    def __init__(self, username, ip_address, port, state):
        self.username = username #username of node
        self.ip_address = ip_address #ipaddress of node
        self.port = port #port of the node
        self.state = state #status of node
 

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
    def getState(self):
        return self.state
    
    #function changes the status of the node
    def setState(self, newState):
        self.state = newState


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

    

    
    
    
    
