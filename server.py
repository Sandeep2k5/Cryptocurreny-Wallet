import socket
import json
from blockchain import Blockchain  

HOST = "localhost"
PORT = 5000

def handle_client_connection(client_socket, blockchain):
    try:
        data = client_socket.recv(4096).decode()
        received_data = json.loads(data)
        
     
        if received_data.get("type") == "blockchain_data":
           
            new_chain = received_data.get("data", [])
            blockchain.chain = [Block(b["index"], b["previous_hash"], b["data"], b["nonce"]) for b in new_chain]
            client_socket.sendall("Blockchain data received and updated.".encode())
            print("Blockchain data successfully received and updated.")
        else:
            client_socket.sendall("Invalid data type received.".encode())
    except Exception as e:
        print("Error handling client connection:", e)
        client_socket.sendall(f"Error: {e}".encode())
    finally:
        client_socket.close()

def start_server():

    blockchain = Blockchain()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:

            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            handle_client_connection(client_socket, blockchain)

if __name__ == "__main__":
    start_server()
