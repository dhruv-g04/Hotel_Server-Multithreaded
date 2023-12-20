import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8888))

    # Get and Send username to the server
    username = input("Enter your username: ")
    client_socket.send(username.encode("utf-8"))

    # Get and Send password to the server
    password = input("Enter your password: ")
    client_socket.send(password.encode("utf-8"))

    while True:
        action = input("Enter action ('book' to book rooms, 'checkout' to checkout from all booked rooms, 'query' to check room number, 'exit' to quit): ")
        
        if action.startswith("book"):
            # Extract the number of rooms from user input
            num_rooms = input("Enter the number of rooms to book: ")
            action = f"{action} {num_rooms}"

        # Send the action to the server
        client_socket.send(action.encode("utf-8"))
        if action == "exit":
            break


        # If the action is 'query' or 'book', receive the server's response
        response = client_socket.recv(1024).decode("utf-8")
        print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    main()

