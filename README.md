# CECS327_SP25_Group47


## Team Members
- David Rivera
- Prajwal Sharma

## Project Description
This project will help us with:
1. Learning  how to integrate IoT sensors and databases into a functional system.
2. Improving  your TCP client-server communication skills with real-world IoT data.
3. Understanding and utilize metadata for IoT devices to enhance system flexibility.
4. Performing  data analysis and unit conversions in response to user queries.
5. Gaining hands-on experience with cloud deployment and system integration.
Using:
TCP Client/Server communication
IoT sensor data
PostgreSQL database
Metadata from Dataniz


## How to Run
1. Clone the repository
2. Start the database:
update the database connection credentials in server.py
3. Run the server.py:
listen for tcp connections
process valid Iot queries
uses json and metadata to respond
4. Run the client:
   eneter the following queries:
1. What is the average moisture inside my kitchen fridge in the past three hours?
2. What is the average water consumption per cycle in my smart dishwasher?
3. Which device consumed more electricity among my three IoT devices (two
refrigerators and a dishwasher)?
5. Metadata usage: board names, sensor types is used to filter and query relevant sensor data, convert units, and align timestamps to pst


Running client: 
1. open a command prompt window
Run the server: python server.py and type in any port number and wait for client conection
Run client.py and enter the server ip adress and port number and hit ENTER.

-david
