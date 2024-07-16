import socket
import threading
import sys
import os
sys.path.append("..")
from recommendation_system.setup_database import DatabaseServices
from services.role_service import RoleServices
from services.user_services import UserServices
from services.login import AuthenticationService
from services.admin import AdminHandler
from services.employee_services import EmployeeService
from services.chef import ChefService

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

# Get the script directory and construct the path to the database
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..', 'services', 'recommendation_engine.db')
db_path = os.path.normpath(db_path)

# Initialize database services and other necessary services
db = DatabaseServices(db_path)
role_services = RoleServices(db)
user_services = UserServices(db)
auth_service = AuthenticationService(user_services)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        try:
            while True:
                conn.sendall("Please enter your email:".encode())
                email = conn.recv(1024).decode().strip()
                if not email:
                    break
                print(f"Email received from {addr}: {email}")

                user = auth_service.authenticate_user(email)
                if user:
                    user_id = user[0]
                    role_id = user[2]
                    role_name = role_services.get_role_name_by_id(role_id)
                    break
                else:
                    print(f"User with email {email} doesn't exist")
                    conn.sendall("User doesn't exist. Please enter your email again:".encode())
            
            conn.sendall(f"Your role is: {role_name}".encode())

            if role_name == "admin":
                admin_handler = AdminHandler(db)
                while True:
                    conn.sendall(admin_handler.show_admin_options().encode())
                    choice = conn.recv(1024).decode().strip()
                    if not choice:
                        break
                    admin_handler.handle_choice(conn, choice)

            elif role_name == "employee":
                employee_handler = EmployeeService(db)
                user_id = user[0]
                while True:
                    conn.sendall(employee_handler.show_employee_options().encode())
                    choice = conn.recv(1024).decode().strip()
                    if not choice:
                        break
                    employee_handler.handle_choice(conn, choice,user_id)

            elif role_name == "chef":
                chef_handler = ChefService(db)
                while True:
                    conn.sendall(chef_handler.show_chef_options().encode())
                    choice = conn.recv(1024).decode().strip()
                    if not choice:
                        break
                    chef_handler.handle_choice(conn, choice)

            else:
                role_name = "guest"
        except ConnectionResetError:
            print(f"Connection with {addr} was reset.")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            print(f"Connection with {addr} closed.")
            conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started and listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
