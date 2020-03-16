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
        return {"code":"FAILURE: not a registered user", "node":"empty"}
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


def state(Data):
    username = Data[0]
    keys = dht.get_reg_nodes().keys()

    #check if user is registered
    if (username not in keys):
        return {"code":"FAILURE: not a registered user", "node":"empty"}

    else:
        Obj = dht.get_reg_nodes()[username]
        if (Obj.getState() == "InDHT"):
            return {"code":"SUCCESS", "node":"empty"}


#dht complete function to check if dht requirements are satisfied
def dhtComplete(Data):
    #check if user is registered
    username = Data[0]
    keys = dht.get_reg_nodes().keys()
    if (username in keys):
        if (dht.get_dht_node()):
            nodeobj = dht.get_dht_node()[0]
            #check if the user is a leader
            if (nodeobj.getState() != 'Leader'):
                return {"code":"FAILURE"}
            else:
                dht.set_dht_complete(True)
    
    return {"code": "SUCCESS"}


#query function for retriving information from dht
def query(Data):
    #check if user is registered
    if(dht.get_dht_completed()):
        username = Data[0]
        keys = dht.get_reg_nodes().keys()
        if (username in keys):
            nodeobj = dht.get_reg_nodes()[username]
            if(nodeobj.getState() == 'Free'):
                index = random.randint(1,len(dht.get_dht_node()))
                query_node = dht.get_dht_node()[index]
                node_tuple = {"username":query_node.getUsername(),"ip":query_node.getIpAddress(),"port":query_node.getPort()}
                return {"code":"SUCCESS", "node":node_tuple}
            else:
                return  {'code': "FAILURE: node is not free"}
        else:
            return {'code': "FAILURE: user is not registered"}
    else:
        return {'code': "FAILURE: dht is not complete"}

def deregister(Data):
    username = Data[0]
    keys = dht.get_reg_nodes().keys()

    if (username in keys):
        nodeobj = dht.get_reg_nodes()[username]
        if(nodeobj.getState() == 'Free'):    
            dht.get_reg_nodes().pop(username)
            return {"code":"SUCCESS"}
        else:
            return {'code': "FAILURE: node is not free"}
    else:
        return {'code': "FAILURE: user is not registered"}


#function for leaving the dht
def leave(Data):
    if (dht.get_dht_completed()):
        username = Data[0]
        keys = dht.get_reg_nodes().keys()
        if (username in keys):
            nodeobj = dht.get_reg_nodes()[username]
            if (nodeobj.getState() == 'Leader'):
                #keep record of right node of the user
                right = nodeobj.get_right_node()
                #intiate teardown procedure
                nodeobj.teardown(Data)
                #deleting local hash table after teardown propagates back to Leader
                #nodeobj.delete(local_hash_table)
                #renumbering and resetting leader
                nodeobj.resetID()
                #resetting right and left neighbours
                nodeobj.reset_left()
                nodeobj.reset_right()
                #teardown complete command
                teardown_complete(username)
                #rebuilding the dht
                rebuildDHT(Data)
                dht_rebuilt(Data)
            else:
                return {'code':"FAILURE", 'error': "user not DHT leader."}
    else:
        return {'code':"FAILURE", 'error': "DHT not complete."}
    return {'code': "SUCCESS"} 
    leaving = username


#teardown function
# def teardown(Data):
#     username = Data[0]
#     dhtKeys = dht_node.keys()
#     leader = reg_node[username]
#     right = leader.get_right_node()
#     #initiate teardown
#     while (right != leader): 
#         nodeinUse = right
#         right.delete(local_hash_table)
#         nodeinUse.delete(ID)
#         nodeinUse.delete(nodeinUse.get_right_node())
#         nodeinUse.delete(nodeinUse.get_left_node())
#         right = nodeinUse.get_right_node()
#         teardown(right)



#teardown complete function
# def teardown_complete(Data):
#     #check if user is registered
#     username = Data[0]
#     keys = reg_nodes.keys()
#     if (username in keys):
#         nodeobj = reg_node[username]
#         #check if the user is a leader
#         if (nodeobj.getStatus() != 'Leader'):
#             return {'code': "FAILURE"}
        
#     teardown_complete = True
#     for i in dht_node.keys():
#         i.setStatus('Free')
#     dht_completed = False
    
#     return {'code': "SUCCESS"}


# #function for rebuilding the dht
# def rebuildDHT():
#     Leader = Data[1]
#     keys = reg_nodes.keys()
#     if (Leader in keys):
#         nodeobj = reg_node[username]
#         if(dht_completed == False):
#             setUp(Leader)
#             dhtComplete(Leader)
#     dht_rebuilt(Data)
#     pass


#dht rebuilt confirmation
# def dht_rebuilt(Data):
#     #check if user is registered
#     #This needs fixing, still working on this idea
#     newLead = Data[1]
#     checkName = Data[0]
#     keys = reg_nodes.keys()
#     if (checkName != leaving):
#         return "FAILURE"
#     else:
#         checkName.setState("Free")
#         return {'code': "SUCCESS"}
#     pass


#function for resetting ID
# def resetID(Data):
#     username = Data[0]
#     nodeobj = reg_node[username]
#     right = nodeobj.get_right_node()

#     #reduce ring size of the right node
#     while(right != nodeobj):
#         right.get_ring_size()
#         right.get_id()
#         right.id = right.set_id(int(right.get_id) - 1)
#         right.ring_size = right.set_ring_size(int(right.get_ring_size)-1)
#         resetID(right)  
#     pass


# #function for resetting left
# def reset_left(Data):
#     username = Data[0]
#     nodeobj = reg_node[username]
#     left = nodeobj.get_left_node()
#     left.set_right_node(nodeobj.get_right_node())
#     pass


# #function for resetting right
# def reset_right(Data):
#     username = Data[0]
#     nodeobj = reg_node[username]
#     right = nodeobj.get_left_node()
#     right.set_left_node(nodeobj.nodeonj.get_right_node())
#     pass

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

    elif command == 'listen':
        return state(DataArr)
    
##    elif command == 'leave-dht':
##        #calls the query function
##        return query(DataArr)
    
##    elif command == 'dht-rebuilt':
##        #calls the query function
##        return query(DataArr)
    
    elif command == 'deregister':
        #calls the query function
        return deregister(DataArr)
    
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

    

    
    
    
    
