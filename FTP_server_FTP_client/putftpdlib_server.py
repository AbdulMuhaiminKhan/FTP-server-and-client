import os
import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
start_message = "FTP server started. IP: 0.0.0.0, Port: 21"
active_connections = 0
class CustomHandler(FTPHandler):
    def on_connect(self):
        global active_connections
        active_connections +=1
        print(f"client connected from {self.remote_port} {self.remote_ip}")
        print(f"Active users {active_connections}")
    def on_disconnect(self):
        global active_connections
        active_connections -=1
        print(f"client disconnected from {self.remote_port} {self.remote_ip}")
        print(f"Active users {active_connections}")
    def on_login(self, username):
        print(f"User {username} logged in")
    def on_logout(self, username):
        print(f"User {username} logged out")
        
def load_users_from_list(authorizer, filename):
    print(f"loading users from the {filename}")
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            username, password, homedir, perm = line.split(' ')
            if username == 'anonymous':
                authorizer.add_anonymous(homedir, perm=perm)
                logging.info(f'anonymous user, folder {homedir}')
            else:
                authorizer.add_user(username, password, homedir, perm=perm)
                logging.info(f'non-anonymous user, folder {username}')
def main():
    log_file_path = "/Users/emil/Desktop/ftp_with_pytftpdlib/ftp_server.log"
    logging.basicConfig(filename = log_file_path, level=logging.INFO, 
                        format= "%(asctime)s - %(levelname)s - %(message)s")
    
    list_of_guests = DummyAuthorizer()
    users_file_path = os.path.join(os.path.dirname(__file__), "users.ini")
    load_users_from_list(list_of_guests, users_file_path)

    handler = CustomHandler
    handler.authorizer = list_of_guests

    handler.banner = "Welcome to our server"
    print(handler.banner)
    # IP , port number
    server = FTPServer(("0.0.0.0", 21), handler)

    #max connncetion set.
    server.max_cons = 256
    server.max_cons_per_ip = 5

    #start_message = "FTP server started. IP: 0.0.0.0, Port: 21"
    print(start_message)
    logging.info(start_message)
    print("Server is running. Press control + C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        None
    finally:
        print(" User pressed ctrl+C. Server is shutting down.")
        server.close_all()

if __name__ == "__main__":
    main()


