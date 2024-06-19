import socket
import threading
import sys
import os
sys.path.append("..")
from recommendation_system.setup_database import DatabaseServices
from services.role_service import RoleServices
from services.user_services import UserServices
# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the database
db_path = os.path.join(script_dir, '..', 'services', 'recommendation_engine.db')
db_path = os.path.normpath(db_path)
# Database initialization
db = DatabaseServices(db_path)
role_services = RoleServices(db)
user_services = UserServices(db)
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        # Request email from the client
        conn.sendall("Please enter your email:".encode())
        email = conn.recv(1024).decode().strip()
        print(f"Email received from {addr}: {email}")
        
        # Determine the role based on the email
        role_id = role_services.get_role_id_by_email(email)
        if role_id:
            role_name = role_services.get_role_name_by_id(role_id)
        else:
            role_name = "guest"

        conn.sendall(f"Your role is: {role_name}".encode())

        if role_name == "admin":
            options = "1. Add item\n2. Delete item\n3. Update item\nEnter your choice:"
        elif role_name == "employee":
            options = "1. View menu\n2. Choose item\n3. Provide feedback\nEnter your choice:"
        elif role_name == "chef":
            options = "1. Roll out menu\n2. See response\nEnter your choice:"
        else:
            options = "Unknown role. Connection closing."
            conn.sendall(options.encode())
            return

        conn.sendall(options.encode())

        while True:
            data = conn.recv(1024)
            if not data:
                break
            choice = data.decode().strip()
            response = f"You selected: {choice}"
            conn.sendall(response.encode())

    print(f"Connection with {addr} closed")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
