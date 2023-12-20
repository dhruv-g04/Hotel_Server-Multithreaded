import socket
import threading

MAX_ROOMS = 10

def initialize_rooms(total_rooms):
    # Initialize a list of rooms with their numbers and initial occupancy status
    return [{"room_number": i + 1, "is_occupied": False} for i in range(total_rooms)]

def book_rooms(rooms, num_rooms, username, password):
    # Attempt to book the specified number of rooms for the user
    booked_rooms = []
    for room in rooms:
        if not room["is_occupied"]:
            room["is_occupied"] = True
            booked_rooms.append(room["room_number"])
            if len(booked_rooms) == num_rooms:
                break

    # If rooms are booked, assign the room numbers to the user
    if booked_rooms:
        assign_room(username, password, booked_rooms)

    return booked_rooms

def check_out_rooms(rooms, username):
    # Check out rooms previously booked by the user
    user_rooms = user_info.get(username, {}).get("room_numbers", [])
    checked_out_rooms = []

    for room_number in user_rooms:
        for room in rooms:
            if room["room_number"] == room_number and room["is_occupied"]:
                room["is_occupied"] = False
                checked_out_rooms.append(room_number)
    # Clear user's room numbers after check out
    if username in user_info:
        user_info[username]["room_numbers"] = []
    return checked_out_rooms

def assign_room(username, password, room_numbers):
    # Assign booked room numbers to the user
    if username not in user_info:
        user_info[username] = {"password": password, "room_numbers": []}
    
    user_info[username]["room_numbers"].extend(room_numbers)

def query_room(username, password):
    # Query and return information about the user's booked rooms
    if username in user_info and user_info[username]["password"] == password:
        if user_info[username]["room_numbers"]:
            return f"Query result: Room numbers for {username} are {', '.join(map(str, user_info[username]['room_numbers']))}."
        else:
            return f"Query result: {username} has not booked any rooms."
    else:
        if username not in user_info:
            return f"Query result: {username} has not booked any rooms."
        else:
            return f"Query result: Invalid username or password."

def handle_client_messages(client_socket, rooms):
    # Receive username and password from the client
    username = client_socket.recv(1024).decode("utf-8")
    password = client_socket.recv(1024).decode("utf-8")
    
    print(f"User {username} connected")

    while True:
        action = client_socket.recv(1024).decode("utf-8")
        
        if action.startswith("book"):
            try:
                num_rooms = int(action.split()[-1])
                if num_rooms <= 0:
                    client_socket.send("Please specify a valid number of rooms.".encode("utf-8"))
                    continue
                
                booked_rooms = book_rooms(rooms, num_rooms, username, password)
                
                if booked_rooms:
                    response = f"Rooms booked successfully. Your room numbers are: {', '.join(map(str, booked_rooms))}."
                else:
                    response = "Sorry, no rooms are currently available."
                
                client_socket.send(response.encode("utf-8"))

            except ValueError as e:
                #print(f"Error: {e}")
                client_socket.send("Invalid input.".encode("utf-8"))
        elif action == "checkout":
            checked_out_rooms = check_out_rooms(rooms, username)
            if len(checked_out_rooms) > 0:
                response = (
                    f"Rooms checked out successfully. Released room numbers are: {', '.join(map(str, checked_out_rooms))}."
                )
            else:
                response = f"Checkout result: {username} has not booked any rooms."
            client_socket.send(response.encode("utf-8"))
        elif action == "query":
            query_result = query_room(username, password)
            #print(query_result)
            client_socket.send(query_result.encode("utf-8"))

        elif action == "exit":
            break
        else:
            client_socket.send("Invalid input.".encode("utf-8"))

    print(f"User {username} disconnected.")

def main():
    global user_info
    user_info = {}
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8888))
    server_socket.listen()

    print("Server is listening for incoming connections...")

    rooms = initialize_rooms(MAX_ROOMS)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_thread = threading.Thread(target=handle_client_messages, args=(client_socket, rooms))
        client_thread.start()

if __name__ == "__main__":
    main()

