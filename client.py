import socket
import threading

def print_msg(msg):
    print(f" >> {msg}")

alias = ""
while alias != 'y' and alias != 'n':
    alias = input("add alias y/n? ").lower()

if alias == 'y':
    alias = input("add alias: ")
    print(f"alis: '{alias}'")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 4872))
# client.connect((alias, 4872))

while True:
    msg = input("> ")
    client.send(msg.encode())
    data = client.recv(1024)
    # print(f"\t>> {repr(data)}")
    threading.Thread(target=print_msg, args=repr(data))