#Hotel Booking System

This project implements a simple hotel booking system with a server (`hotel_server.py`) and a client (`hotel_client.py`) using Python's socket and threading modules.

## Server (`hotel_server.py`)

### Features
- Book multiple hotel rooms.
- Check out from all booked rooms.
- Query the room numbers booked by a user.
- Handle multiple client connections concurrently using threading.

### Usage
   Run the server script on the host machine.
   ```bash
   python3 hotel_server.py
   ```

   Connect clients to the server using the client script (hotel_client.py).

###Server Implementation

    initialize_rooms(total_rooms):
    Initializes a list of rooms with room numbers and initial occupancy status.

    book_rooms(rooms, num_rooms, username, password):
    Attempts to book the specified number of rooms for the user.

    check_out_rooms(rooms, username):
    Checks out rooms previously booked by the user.

    assign_room(username, password, room_numbers):
    Assigns booked room numbers to the user.

    query_room(username, password):
    Queries and returns information about the user's booked rooms.

    handle_client_messages(client_socket, rooms):
    Handles communication with a connected client, processing user actions.

    main():
    Initializes the server, listens for incoming connections, and spawns threads to handle client messages concurrently.

##Client (hotel_client.py)
###Features

    Connects to the hotel booking server.
    Sends a username and password to the server.
    Supports actions like booking rooms, checking out, querying booked rooms, and exiting.

###Usage

    Run the client script.

    ```bash
    python3 hotel_client.py
    ```

    Enter your username and password.
    Enter actions as prompted.

###Client Implementation

    main():
    Connects to the server, sends username and password, and performs user-specified actions.

#Notes

    Both the server and client scripts need to be running for the hotel booking system to function.
    The server can handle multiple clients concurrently.
    Ensure that the host IP address and port match between the server and client scripts.


