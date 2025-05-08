

import socket

def main():
    host = input("Enter server IP address: ")
    port_str = input("Enter server port number: ")

    try:
        port = int(port_str)
    except ValueError:
        print("Port must be a valid integer.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"Connected to {host}:{port}")

            while True:
                message = input("Enter message to send (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                s.sendall(message.encode())
                data = s.recv(1024)
                print("Received from server:", data.decode())

    except ConnectionRefusedError:
        print("Connection refused. Check if the server is running and the port is correct.")
    except socket.gaierror:
        print("Invalid IP address or hostname.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
