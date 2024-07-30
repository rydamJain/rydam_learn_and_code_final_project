import socket
import threading

# Server configuration
HOST = '172.16.1.100'  # The server's hostname or IP address
PORT = 3000        # The port used by the server

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(f"Received from server: {data.decode()}")
    print("Server connection closed")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        # Start a thread to listen for incoming messages
        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.start()

        # Enter email
        email = input("Please enter your email: ")
        password = input("Please enter your password: ")
        login_details = f"LOGIN;{email};{password}"
        s.sendall(login_details.encode())

        while True:
            name = input("Please enter item name: ")
            price = input("Please enter item price: ")
            availability = input("Please enter item availability: ")
            mealTypeId = input("Please enter meal type ID: ")
            food_item_details = f"admin_addMenuItem;{name};{price};{availability};{mealTypeId}"
            s.sendall(food_item_details.encode())
            message = input("Enter message to send (type 'quit' to exit): ")
            if message.lower() == 'quit':
                print("Closing connection")
                s.shutdown(socket.SHUT_WR)
                break
            
            s.sendall(message.encode())
        
        receive_thread.join()

if __name__ == "__main__":
    main()
