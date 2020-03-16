#This contains client source code
#Authors: Kingsley Besidonne and Molife Chaplain
#Group number: 33
from socket import *
import sys
import csv
import threading
import json
from clientbase import dht
dht = dht()

#port number range [17500,17999]

clientStruct = {}
local_hash_table = {}

#function to set user id, leader sends to dht nodes
def set_id_nodes(nodes):
    #create socket for communicating with clients
    p2pSocket = socket(AF_INET, SOCK_DGRAM)

    for i in range(len(nodes)):
        id = i + 1
        n = int(nodes[i]["ring"])
        left = (i - 1) % n 
        right = (i + 1) % n 
        message = {"id":id, "ring":n, "left_node":nodes[left], "right_node":nodes[right]}
        p2pSocket.sendto(str.encode(message),(nodes[i]["ip"],nodes[i]["port"]))
        
    return {'code': "SUCCESS"}

def set_id(node):
    return True

#function to construct local dht of nodes
def construct_local_dht(data):
    #read in the file
    with open(data[0], newline='') as f:
        reader = csv.reader(f)
        next(f)
        for row in reader:
            record = row
            value = row[3]
            #call the hash function and set value to id_node and pos
            num = hash_function(ord(value),clientStruct['ring'])
            #use id_node to selct node from dht node
            id_node = num[1]
            pos = num[0]
            if (id_node == clientStruct['id']):
                #store record in local hash table
                local_hash_table[pos] = record

    
    return {'code': "SUCCESS"}

#hash function for dht
def hash_function(value, n):
    pos = value %  353
    id_node = pos % n
    return [pos ,id_node]

#controller function for processing client commands
def controller(data):
    DataArr = data.split(" ")
    command = DataArr.pop(0)
    
    if command == "register":
        return {"node":"server", "command":command}

    elif command == "setup-dht":
        return {"node":"server", "command":command}
        
    elif command == 'dht-complete':
        return 'server'
        
    elif command == 'query-dht':
        return 'server'
    
    elif command == "set-id":
        return set_id(DataArr)
    
    elif command == 'construct':
        return construct_local_dht(DataArr)

    elif command == 'listen':
        return {"node":"server", "command":command}
    
    else:
        return "Command is not valid"


def listen():
    #create socket for sending and recieving datagrams
    p2pSocket = socket(AF_INET, SOCK_DGRAM)
    #Bind the local address and port
    server = dht.get_ip()
    port = int(dht.get_port())
    p2pSocket.bind((server,port))
    print("listening...")
    while True:
        data, clientAddr = p2pSocket.recvfrom(2048)
        message = json.dumps(controller(data.decode()))
        if not data:
            break
        p2pSocket.sendto(str.encode(message), clientAddr)

#main function for our code
def main(argv):
    #check if our input parameters are of correct length
    if(len(sys.argv) < 3):
        print("Error: parameter length not correct")
        return 0

    #local address for server
    server = sys.argv[1]
    
    #listening port of server
    port = int(sys.argv[2])
        
    #create socket for sending and recieving datagrams to server
    clientSocket = socket(AF_INET, SOCK_DGRAM) 

    exit_ = True

    while True:
        message = input(">> command(type 'exit' to terminate): ")
        command = controller(message)

        if message == 'exit':
            break

        if command["node"] == 'server':

            clientSocket.sendto(str.encode(message),(server,port))
            data, serverAddr = clientSocket.recvfrom(2048)
            output = json.loads(data.decode())

            if(command["command"] == "register"):
                dht.set_ip(output["node"]["ip"])
                dht.set_port(output["node"]["port"])
                print(output["code"])
                
            elif(command["command"] == "setup-dht"):
                if(output["code"] == "SUCCESS"):
                    print("setup")
                else:
                    print(output["code"])

            elif(command["command"] == "listen"):
                if(output["code"] == "SUCCESS"):
                    exit_ = False
                    break

    if (not(exit_)):
        listen()
  
if __name__ == '__main__' :
    main(sys.argv)
