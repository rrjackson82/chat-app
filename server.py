import socket
import threading
import datetime

# Shared list of (conn, addr) tuples for every connected client
clients = []
# Lock so threads don't corrupt the clients list when adding/removing simultaneously
clients_lock = threading.Lock()

def log_chat(msg="err1 no data"):
    with open('chatlogs.txt', 'a') as f:
        if f:
            f.write('\n'+msg)

def broadcast(message, sender_conn=None):
    # Send the message to every client except the one who sent it
    with clients_lock:
        for conn, addr in clients:
            if conn != sender_conn:
                try:
                    conn.sendall(message.encode())
                except:
                    pass

def handle_client(conn, addr):
    # Runs in its own thread — one per connected client
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    print(f"Connected {addr}")
    log_chat(f"@{now}: Connected {addr}")

    # Register this client so broadcast() can reach it
    with clients_lock:
        clients.append((conn, addr))

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                # Empty recv means the client disconnected
                break
            msg = data.decode()
            # Prefix the sender's IP so recipients know who wrote it
            formatted = f"{addr[0]}: {msg}"
            print(formatted)
            log_chat(f"{addr[0]}@{now}: {msg}")
            broadcast(formatted, sender_conn=conn)
    finally:
        # Always clean up, even if an exception occurs
        with clients_lock:
            clients.remove((conn, addr))
        conn.close()
        print(f"Disconnected {addr}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 4872))
server.listen()
print("Listening on port 4872...")

while True:
    # Block until a new client connects, then hand it off to a thread
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
