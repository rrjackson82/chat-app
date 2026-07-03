import socket
import threading
import datetime

def log_chat(msg="err1 no data"):
    with open('chatlogs.txt', 'a') as f:
        if f:
            f.write('\n'+msg)
        
def handle_client(conn, addr):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    print(f"Connected {addr}")
    log_chat(f"@{now}: Connected {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"{addr}: {data.decode()}")
        log_chat(f"{addr[0]}@{now}: {data.decode()}")
        conn.sendall(data)
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 4872))
server.listen()
print("Listening on port 4872...")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()