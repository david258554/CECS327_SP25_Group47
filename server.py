# David Rivera
# Darrel Dennis
# CECS 327
import socket
import psycopg2 # DARREL: For connecting to Neon and SQL

# GOALS:
# 2. Impliment a menu that returns the results of these functions

def calculate_avg_fridge_moisture(connection):
    # DARREL: This function calls a query onto the passed connection peram, query calculates the average and prints it
    #         The units are relative, with values ranging between 0 (0%) and 40 (100%)
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT AVG((payload->>'Moisture Meter - moist-sensor_refrigerator_01')::numeric) AS moisture
                   FROM neon_table_virtual 
                   WHERE payload->>'board_name' = 'arduino_refrigerator_01' 
                   AND time > NOW() - INTERVAL '3 hours'; 
                   """)
    out = cursor.fetchone()[0]
    cursor.close()
    return(float(out))

def calculate_avg_water_consuption_per_cycle_dishwasher(connection):
    # DARREL: This function calls a query onto the passed connection peram, query calculates the average and prints it
    #         The units are liters per min
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT AVG((payload->>'YF-S201 - water-flow-sensor_dishwasher_01')::numeric) AS moisture_percent 
                   FROM neon_table_virtual 
                   WHERE payload->>'board_name' = 'arduino_dishwasher_01';
                   """)
                   # DARREL: Unsure to add "AND time > NOW() - INTERVAL '3 hours';" or any time limit
                   #         Currently it just calculates the average of all time
    out = cursor.fetchone()[0]
    cursor.close()
    return(float(out))

def calculate_most_electicity_consumed(connection):
    # DARREL: This function calls a query onto the passed connection peram, query calculates the average and prints it
    #         The units are current in amperes
    cursor = connection.cursor()

    # DARREL: Return amperes from arduino_refrigerator_01
    cursor.execute("""
                   SELECT (payload->>'ACS712 - ammeter_refrigerator_01')
                   FROM neon_table_virtual
                   WHERE payload->>'board_name' = 'arduino_refrigerator_01'
                   ORDER BY time DESC LIMIT 1;
                   """)
    refrig_01_amperes = float(cursor.fetchone()[0])

    # DARREL: Return amperes from arduino_refrigerator_02
    cursor.execute("""
                   SELECT (payload->>'ACS712 - ammeter_refrigerator_02')
            FROM neon_table_virtual
            WHERE payload->>'board_name' = 'arduino_refrigerator_02'
            ORDER BY time DESC LIMIT 1;
                   """)
    refrig_02_amperes = float(cursor.fetchone()[0])

    # DARREL: Return amperes from arduino_dishwasher_01
    cursor.execute("""
                   SELECT (payload->>'ACS712 - ammeter_dishwasher_01')
            FROM neon_table_virtual
            WHERE payload->>'board_name' = 'arduino_dishwasher_01'
            ORDER BY time DESC LIMIT 1;
                   """)
    diwash_01_amperes = float(cursor.fetchone()[0])

    cursor.close()

    # DARREL: Compare and return largest
    if refrig_01_amperes > refrig_02_amperes and refrig_01_amperes > diwash_01_amperes:
        return("Largest last reported amperes is \"refrigerator_01\" with: " + str(refrig_01_amperes))
    elif refrig_02_amperes > refrig_01_amperes and refrig_02_amperes > diwash_01_amperes:
        return("Largest last reported amperes is \"refrigerator_02\" with: " + str(refrig_02_amperes))
    else:
        return("Largest last reported amperes is \"dishwasher_01\" with: " + str(diwash_01_amperes))

def inital_test(connection):
    # DARREL: This function will call each function, output their results, then go to the start_server function.
    #         Using this primarly to just test the functions without connecting a client.
    print("")
    print("RUNNING INITAL TESTS:")
    print("     -CALLING FUNCTION: calculate_avg_fridge_moisture (Relative (0-40))")
    print(calculate_avg_fridge_moisture(connection))
    print("     -CALLING FUNCTION: calculate_avg_water_consuption_per_cycle_dishwasher (Liters per Min)")
    print(calculate_avg_water_consuption_per_cycle_dishwasher(connection))
    print("     -CALLING FUNCTION: calculate_most_electicity_consumed (Amperes)")
    print(calculate_most_electicity_consumed(connection))
    print("")

def start_server():
    try:
        # DARREL: Setup query connection
        connecturl = "postgresql://read_only_user:readonlypassyay11124@ep-curly-cloud-a6wcg53n-pooler.us-west-2.aws.neon.tech/neondb?sslmode=require"
        connection = psycopg2.connect(connecturl)

        # DARREL: Run every function just to test database connection and queries!
        inital_test(connection)

        # DARREL: This the old server code block!
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

        # DARREL: Close query connection
        connection.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        incomingSocket.close() # Close client connection
        myTCPSocket.close() # Close server socket
        connection.close() # DARREL: Close query connection

if __name__ == "__main__":
    start_server()
