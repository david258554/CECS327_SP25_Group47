import socket #for creating tcp server socket
import psycopg2 # for postgresSQl database
import os
from datetime import datetime

# This is the connection string used to connect to the PostgreSQL database
DB_URL = "postgresql://neondb_owner:npg_Ma6fxrsweH2A@ep-proud-sun-a4gsaw7j-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
#dictionary of allowed queries 
ALLOWED_QUERIES = {
    #query 1
    "What is the average moisture inside my kitchen fridge in the past three hours?": """
        SELECT AVG((kv.value)::NUMERIC) AS avg_moisture 
        FROM "IOTDATA_virtual"
        CROSS JOIN LATERAL jsonb_each_text(payload::JSONB) AS kv(key, value)
        WHERE payload::jsonb->>'board_name' = 'Fridge1Rasberry'
        AND kv.key = 'DHT11 - Fridge1DHT11Humidity'
        AND time > NOW() - INTERVAL '3 hours';
    """,
     #query 2
    "What is the average water consumption per cycle in my smart dishwasher?": """
        SELECT AVG(CAST(payload::jsonb->>'YF-S201 - DishwasherYFS201WATERFLOW' AS FLOAT))
        FROM "IOTDATA_virtual"
        WHERE payload::jsonb->>'board_name' = 'DishwasherRasberry';
    """,
    #query 3
    "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?": """
        SELECT payload::jsonb->>'board_name' as board_name, 
        ABS(AVG(CAST(payload::jsonb->>'ACS712 - Fridge1ACS712Current' AS FLOAT))) AS avg_current
        FROM "IOTDATA_virtual"
        WHERE payload::jsonb->>'board_name' IN ('Fridge1Rasberry', 'Fridge2Rasberry', 'DishwasherRasberry')
        AND (payload::jsonb->>'ACS712 - Fridge1ACS712Current') ~ '^[0-9.]+$'
        GROUP BY payload::jsonb->>'board_name'
        ORDER BY avg_current DESC
        LIMIT 1;
    """
}


# percentage (1)
# liters per min for (2)

#function to process incoming queries
def process_query(query):
    # Check if the query is supported
    if query not in ALLOWED_QUERIES:
        return ("Unsupported query. Please use one of the following:\n" +
                "\n".join(f"- {q}" for q in ALLOWED_QUERIES))

    try:
        # Connect to the database
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        # Execute the query associated with the input
        cur.execute(ALLOWED_QUERIES[query])
        result = cur.fetchone()
        cur.close()
        conn.close()

        # Return formatted result
        if result and result[0] is not None:
            return f"Query result: {result[0]:.2f}" if isinstance(result[0],
                                                                  (float, int)) else f"Query result: {result[0]}"
        else:
            return "No data available for this query."

    except Exception as e:
        return f"Error processing query: {e}"

#main function to run the tcp server
def main():
    # Create a TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Accept IP and port input from user for flexibility
    host = input("Enter IP address to bind (leave blank for all interfaces): ") or ""
    port = int(input("Enter port number to listen on: "))
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host or '0.0.0.0'}:{port}")

    try:
        while True:
            # Accept new client connections
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr[0]}:{addr[1]}")

            while True:
                # Receive data from client
                data = client_socket.recv(2048).decode().strip()
                if not data:
                    break
                print(f"Received: {data}")
                # Process the query and send response
                response = process_query(data)
                client_socket.sendall((response + "\n").encode())

            # Close client connection
            client_socket.close()
            print("Client disconnected.")
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        # Ensure server socket is closed on exit
        server_socket.close()


if __name__ == "__main__":
    main()
