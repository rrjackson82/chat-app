import socket
import threading


def print_msg(msg):
    print(f" >> {msg}")


def receive_loop(sock):
    # Runs in a background thread — continuously listens for incoming messages
    # so the main thread stays free for user input
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                # Server closed the connection
                break
            print_msg(data.decode())
        except:
            break


alias = ""
while alias != "y" and alias != "n":
    alias = input("add alias y/n? ").lower()

if alias == "y":
    alias = input("add alias: ")
    print(f"alias: '{alias}'")


host = input("Server IP (leave blank for localhost): ").strip() or "127.0.0.1"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 4872))

# Start the receiver as a daemon thread so it exits automatically when the main thread exits
threading.Thread(target=receive_loop, args=(client,), daemon=True).start()

# Main thread: just handles user input and sends messages
while True:
    msg = input("> ")
    client.send(msg.encode())
