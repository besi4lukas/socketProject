#This contains client source code
import socket
import sys



#main function for our code
def main(argv):
    #input from command line

    #check if our input parameters are of correct length
    if(len(sys.argv) < 3):
        print("Error: parameter length not correct")

    #local address for server
    server = sys.argv[1]
    
    #listening port of server
    port = sys.argv[2]
        
    #create socket for sending and recieving datagrams
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #connect to local address and port  
        sock.connect((server,port))
        while True:
            message = input(">> command: ")
            sock.sendall(message)
            data = sock.recv(1024)
            print(repr(data))

  
if __name__ == '__main__' :
    main(sys.argv)


    

    

    
    
