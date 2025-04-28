import socket

def start_client():
    try:
        serverIP = input("Enter server IP address: ")
        serverPort = int(input("Enter server port number: "))
        myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myTCPSocket.connect((serverIP, serverPort)) # Connect to the server
        print(f"Connected to server at {serverIP}:{serverPort}")
        while True:
            someData = input("Enter a message to send (or type 'exit' to quit): ")
            if someData.lower() == "exit":
                print("Closing connection.")
                break
            # Send the message as a bytearray
            myTCPSocket.send(bytearray(str(someData), encoding='utf-8'))
            # Receive server response
            maxBytesToReceive = 1024
            serverResponse = myTCPSocket.recv(maxBytesToReceive).decode('utf-8')
            print(f"Server reply: {serverResponse}")
    except ValueError:
        print("Invalid port number. Please enter a valid number.")
    except ConnectionRefusedError:
        print("Could not connect to the server. Check the IP address and port.")
    except socket.gaierror:
        print("Invalid IP address. Please enter a valid address.")
    except Exception as e:
        print(f"An error occurred: {e}")
    myTCPSocket.close() # Terminate connection with the server

if __name__ == "__main__":
    start_client()
