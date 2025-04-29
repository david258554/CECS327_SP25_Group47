import socket


# 3 queries 
valid_queries = [ 
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "3Which device consumed more electricity among my three IoT devices?"
]

def start_client():
    try:
        serverIP = input("Enter server IP address: ")
        serverPort = int(input("Enter server port number: "))
        myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myTCPSocket.connect((serverIP, serverPort)) # Connect to the server
        print(f"Connected to server at {serverIP}:{serverPort}")

        while True:
            print("\nPlease enter one of the following queries:")
            for query in valid_queries:
                print("-", query)

            someData = input("\nYour query (or type 'exit' to quit): ")
            if someData.lower() == "exit":
                print("Closing connection.")
                break
            #checking if query is valid
            if someData in valid_queries:
                myTCPSocket.send(bytearray(str(someData), encoding='utf-8'))
                maxBytesToReceive = 1024
                serverResponse = myTCPSocket.recv(maxBytesToReceive).decode('utf-8')

                print(f"\n Server reply: {serverResponse}")
            else:
                print("\n Sorry, this query cannot be processed.")
                print("Please try one of the following valid queries:")
                for query in valid_queries:
                    print("-", query)

            
    except ValueError:
        print("Invalid port number. Please enter a valid number.")
    except ConnectionRefusedError:
        print("Could not connect to the server. Check the IP address and port.")
    except socket.gaierror:
        print("Invalid IP address. Please enter a valid address.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        myTCPSocket.close()
if __name__ == "__main__":
    start_client()
