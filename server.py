# David Rivera
# CECS 327
import socket
import psycopg2 # For connecting to Neon and SQL

def calculate_avg_fridge_moisture(connection):
    # units are relative, with values ranging between 0 (0%) and 40 (100%)
    cursor = connection.cursor()

    # UPDATE W/ PROPER SENSOR NAMES AND BOARD NAMES
    cursor.execute("""
                   SELECT AVG((payload->>'moist-sensor_refrigerator_1')::numeric) AS moisture
                   FROM neon_table_virtual 
                   WHERE payload->>'board_name' = 'arduinorefrigerator_1' 
                   AND time > NOW() - INTERVAL '3 hours'; 
                   """)
    
    out = cursor.fetchone()[0]
    cursor.close()
    return((float(out) / 40 * 100)) # This is a percentage!

def calculate_avg_water_consuption_per_cycle_dishwasher(connection):
    # The units are liters per min
    cursor = connection.cursor()

    # UPDATE W/ PROPER SENSOR NAMES AND BOARD NAMES
    cursor.execute("""
                   SELECT AVG((payload->>'water-flow-sensor_dishwasher_1')::numeric) AS moisture_percent 
                   FROM neon_table_virtual 
                   WHERE payload->>'board_name' = 'arduinodishwasher_1';
                   """)
                   # Currently it just calculates the average of all time

    out = cursor.fetchone()[0]
    cursor.close()
    return(float(out))

def calculate_most_electicity_consumed(connection):
    # units are in kWh
    # these calculations are made with the assumption that 120V (US) and 5A version of the ACS712 was used

    # arduinorefrigerator_2 - UPDATE W/ PROPER SENSOR NAMES AND BOARD NAMES
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT ((SUM((payload->>'ammeter_refrigerator_2')::numeric) - (2.5 * COUNT(*))) / 0.185) * 120 / 60 / 1000 AS kWh
                   FROM neon_table_virtual
                   WHERE payload->>'board_name' = 'arduinorefrigerator_2';
                   """)
    refrig_02 = float(cursor.fetchone()[0])
    cursor.close()
    del cursor

    # arduinorefrigerator_1 - UPDATE W/ PROPER SENSOR NAMES AND BOARD NAMES
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT ((SUM((payload->>'ammeter_refrigerator_1')::numeric) - (2.5 * COUNT(*))) / 0.185) * 120 / 60 / 1000 AS kWh
                   FROM neon_table_virtual
                   WHERE payload->>'board_name' = 'arduinorefrigerator_1';
                   """)
    refrig_01 = float(cursor.fetchone()[0])
    cursor.close()
    del cursor

    # arduinodishwasher_01 UPDATE W/ PROPER SENSOR NAMES AND BOARD NAMES
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT ((SUM((payload->>'ammeter_dishwasher_1')::numeric) - (2.5 * COUNT(*))) / 0.185) * 120 / 60 / 1000 AS kWh
                   FROM neon_table_virtual
                   WHERE payload->>'board_name' = 'arduinodishwasher_1';
                   """)
    diswas_01 = float(cursor.fetchone()[0])
    cursor.close()
    del cursor

    # Compare and return largest
    if refrig_02 > refrig_01 and refrig_02 > diswas_01:
        return("Largest lifetime power draw is \"refrigerator 2\" with: " + str(refrig_02) + " kWh")
    elif refrig_01 > refrig_02 and refrig_01 > diswas_01:
        return("Largest lifetime power draw is \"refrigerator 1\" with: " + str(refrig_01) + " kWh")
    else:
        return("Largest lifetime power draw is \"dishwasher 1\" with: " + str(diswas_01) + " kWh")

def inital_test(connection):
    # Test the functions without connecting a client.
    print("")
    print("RUNNING INITAL TESTS:")
    print("Test 1: calculate_avg_fridge_moisture (Relative (0-40))")
    print(calculate_avg_fridge_moisture(connection))
    print("Test 2: calculate_avg_water_consuption_per_cycle_dishwasher (Liters per Min)")
    print(calculate_avg_water_consuption_per_cycle_dishwasher(connection))
    print("Test 3: calculate_most_electicity_consumed (Amperes)")
    print(calculate_most_electicity_consumed(connection))
    print("")

def start_server():
    try:
        # Setup query connection
        connecturl = "" # Add connection url here
        connection = psycopg2.connect(connecturl)

        # Run every function just to test database connection and queries!
        inital_test(connection)

        # This the old server code block!
        print("RUNNING SERVER CODE:")
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

        # Close query connection
        connection.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        incomingSocket.close() # Close client connection
        myTCPSocket.close() # Close server socket
        connection.close() # Close query connection

if __name__ == "__main__":
    start_server()
