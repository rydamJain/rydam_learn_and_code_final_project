import socket
import threading
import sys
import os
sys.path.append("..")
from recommendation_system.setup_database import DatabaseServices
from services.role_service import RoleServices
from services.user_services import UserServices
from services.login import *

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
auth_service = AuthenticationService(user_services)


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        while True:
            # Request email from the client
            conn.sendall("Please enter your email:".encode())
            email = conn.recv(1024).decode().strip()
            print(f"Email received from {addr}: {email}")

            # Authenticate the user
            user = auth_service.authenticate_user(email)
            if user:
                role_id = user[2]
                role_name = role_services.get_role_name_by_id(role_id)
                break  # Exit the loop if user is found
            else:
                print(f"User with email {email} doesn't exist")
                conn.sendall("User doesn't exist. Please enter your email again:".encode())

        conn.sendall(f"Your role is: {role_name}".encode())

        options = role_services.show_role_based_options(role_name)
        conn.sendall(options.encode())

        if role_name == "guest":
            return

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
        print(f"Server get started and listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
