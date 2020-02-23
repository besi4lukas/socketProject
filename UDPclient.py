#This contains client source code
#Authors: Kingsley Besidonne and Molife Chaplain
#Group number: 33
import socket
import sys

#port number range [17500,17999]

#main function for our code
def main(argv):
    #input from command line

    #check if our input parameters are of correct length
    if(len(sys.argv) < 3):
        print("Error: parameter length not correct")
        return 0

    #local address for server
    server = sys.argv[1]
    
    #listening port of server
    port = int(sys.argv[2])
        
    #create socket for sending and recieving datagrams
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as clientSocket:
        while True:
            message = input(">> Input lowercase command(type 'exit' to terminate): ")
            if message == 'exit':
                break
            clientSocket.sendto(str.encode(message),(server,port))
            data, serverAddr = clientSocket.recvfrom(2048)
            print(data.decode())

  
if __name__ == '__main__' :
    main(sys.argv)
