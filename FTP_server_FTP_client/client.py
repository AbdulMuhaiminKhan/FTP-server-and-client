import ftplib
import os

def simple_ftp_client():
    
    host = input("Enter FTP host (default: localhost): ").strip()
    if not host:
        host = 'localhost'

    port_str = input("Enter FTP port (default: 21): ").strip()
    if not port_str:
        port = 21
    else:
        try:
            port = int(port_str)
        except ValueError:
            print("Invalid port number. Using default 21.")
            port = 21

    username = input("Enter username (default: anonymous): ").strip()
    if not username:
        username = 'anonymous'

    password = input("Enter password (default: 6): ").strip()
    if not password:
        password = '6'

    ftp = ftplib.FTP()
    
    try:
        print(f"Connecting to {host}:{port}...")
        ftp.connect(host, port)
        ftp.login(username, password)
        print(f"Connected to {host}:{port} as {username}")
        
        while True:
            try:
                command = input("ftp> ").strip()
                
                if command.lower() in ['quit', 'exit']:
                    break
                elif command.lower() == 'ls':
                    ftp.retrlines('LIST')
                elif command.lower() == 'pwd':
                    print(ftp.pwd())
                elif command.startswith('cd '):
                    dirname = command[3:].strip()
                    ftp.cwd(dirname)
                    print(f"Changed to {ftp.pwd()}")
                elif command.startswith('lcd '):
                    local_dir = command[4:].strip()
                    try:
                        os.chdir(local_dir)
                        print(f"Local directory changed to {os.getcwd()}")
                    except Exception as e:
                        print(f"Error changing local directory: {e}")
                elif command.startswith('get '):
                    filename = command[4:].strip()
                    with open(filename, 'wb') as f:
                        ftp.retrbinary(f'RETR {filename}', f.write)
                    print(f"Downloaded {filename}")
                elif command.startswith('put '):
                    filename = command[4:].strip()
                    if not os.path.exists(filename):
                        print(f"Error: Local file '{filename}' not found.")
                        continue
                    with open(filename, 'rb') as f:
                        ftp.storbinary(f'STOR {filename}', f)
                    print(f"Uploaded {filename}")
                elif command == 'help':
                    print("Available commands: lcd , ls, pwd, cd <dir>, lcd <local-dir>, get <file>, put <file>, quit, exit")
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("Disconnecting...")
        try:
            ftp.quit()
        except Exception as e:
            print(f"Error disconnecting: {e}") 

if __name__ == "__main__":
    simple_ftp_client()