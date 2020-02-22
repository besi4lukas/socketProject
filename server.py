#This file contains server source code
import socket
import sys
import ipaddress


#dictionary for storing registered nodes and their status

#dictionary for storing nodes in dht


#register function for registering users
def register():
    
    return "SUCCESS"

#setup function for constructing the dht
def setUp():
    
    return "SUCCESS"

#dht complete function to check if dht requirements are satisfied
def dhtComplete():
    
    return "SUCCESS"

#query function for retriving information from dht
def query():
    
    return "SUCCESS"

#controller function for processing client commands
def controller(data):
    
    return "SUCCESS"


#Class nodes for client objects
class node:
    def __init__(self, username, ip_address, port):
        self.username = username
        self.ip_address = ip_address
        self.port = port
        #create local hash table for storing information

    #create hash function
    #define function for inserting into hash table
    #define function for getting information


#main function for our code
def main(argv):
    #check if our commandline input parameters are of correct length
    if(len(sys.argv) != 2):
        print("Error: parameter length not correct")

    #listening port of server
    port = sys.argv[1]

    #local address for server
    hostAddr = str(ipaddress.IPv4Address('127.0.0.1'))
    

    #create socket for sending and recieving datagrams
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((hostAddr,port))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                #message = controller(data)
                if not data:
                    break
                conn.sendall("Received Information")
                
        


    #Bind the local address and port

    #listen and accept

if __name__ == '__main__' :
    main(sys.argv)

    

    
    
    
    
