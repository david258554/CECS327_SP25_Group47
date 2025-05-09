

import socket #import socket

#main function that runs the tcp client
def main():
    #ask user for the server's IP address and port number
    host = input("Enter server IP address: ")
    port_str = input("Enter server port number: ")
    
    #convert the port number to an integer and validate it
    try:
        port = int(port_str)
    except ValueError:
        print("Port must be a valid integer.")
        return  #stop the program if the port is not valid


    try:
        #ctreate a tcp socket using ipv4
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"Connected to {host}:{port}")
            
            #loop to send messages continously
            while True:
                message = input("Enter message to send (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                #send the message to the server    
                s.sendall(message.encode())
                data = s.recv(1024)
                print("Received from server:", data.decode())
    #handle common connection errors
    except ConnectionRefusedError:
        print("Connection refused. Check if the server is running and the port is correct.")
    except socket.gaierror:
        print("Invalid IP address or hostname.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
