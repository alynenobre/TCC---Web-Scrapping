import socket

try:
    ip = socket.gethostbyname("sterling-cooper-atlas.nomic.ai")
    print(f"O IP do host é: {ip}")
except socket.gaierror:
    print("Falha ao resolver o nome do host.")
