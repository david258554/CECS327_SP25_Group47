#David Rivera
#cecs 327 assignment 5
# due: 3/16/2025
import socket
import psycopg2 # DARREL: For connecting to Neon and SQL

# GOALS:
# 1. Impliment a function for each of these
#   a. What is the average moisture inside my kitchen fridge in the past three hours?
#   b. What is the average water consumption per cycle in my smart dishwasher?
#   c. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?
# 2. Impliment a menu that returns the results of these functions

def calculate_avg_fridge_moisture(connection):
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT payload->>'Moisture Meter - moist-sensor_refrigerator_01' AS moisture_percent 
                   FROM neon_table_virtual WHERE payload->>'board_name' = 'arduino_refrigerator_01' 
                   AND time > NOW() - INTERVAL '3 hours'; 
                   """)
    print(cursor.fetchone())
    cursor.close()

    print("FUNCTION CALLED: calculate_avg_fridge_moisture")

def calculate_avg_water_consuption_per_cycle_dishwasher(connection):
    print("FUNCTION CALLED: calculate_avg_water_consuption_per_cycle_dishwasher")

def calculate_most_electicity_consumed(connection):
    print("FUNCTION CALLED: calculate_most_electicity_consumed")

def inital_test():
    # DARREL: This function will call each function, output their results, then go to the start_server function.
    # DARREL: Using this primarly to just test the functions without connecting a client.

    try:
        connecturl = "postgresql://neondb_owner:npg_8cHZMibC2QVt@ep-curly-cloud-a6wcg53n-pooler.us-west-2.aws.neon.tech/neondb?sslmode=require"
        connection = psycopg2.connect(connecturl)

        print("CALLING FUNCTION: calculate_avg_fridge_moisture")
        calculate_avg_fridge_moisture(connection)

        print("CALLING FUNCTION: calculate_avg_water_consuption_per_cycle_dishwasher")
        calculate_avg_water_consuption_per_cycle_dishwasher(connection)

        print("CALLING FUNCTION: calculate_most_electicity_consumed")
        calculate_most_electicity_consumed(connection)

        connection.close()
    
    except Exception as error:
        print(f"Error connecting to SQL: {error}")

def start_server():
    try:
        myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow user to enter a port instead of hardcoding
        serverPort = int(input("Enter the port number to run the server on: "))
        myTCPSocket.bind(('0.0.0.0', serverPort)) # Binds to localhost
        myTCPSocket.listen(5) # Allows up to 5 connections in queue
        print(f"Server is running on port {serverPort}... Waiting for connections.")
        incomingSocket, incomingAddress = myTCPSocket.accept()
        print(f"Connection established with {incomingAddress}")
        while True:
            numberOfBytes = 1024 # Maximum bytes to receive
            myData = incomingSocket.recv(numberOfBytes).decode('utf-8') # Receive message from client
            if not myData: # If client disconnects
                print("Client disconnected.")
                break
            print(f"Received from client: {myData}")
            # Convert the received message to uppercase and send it back
            response = myData.upper()
            incomingSocket.send(bytearray(response, encoding='utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")
        incomingSocket.close() # Close client connection
        myTCPSocket.close() # Close server socket

if __name__ == "__main__":
    inital_test()
    start_server()
