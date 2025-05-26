# edge_device/communication/edge_to_edge.py

import socket
import threading
import json

class EdgeToEdgeComm:
    def __init__(self, host='0.0.0.0', port=6000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.peers = []

    def start_server(self):
        """Start server to listen for incoming connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[EdgeToEdge] Listening on {self.host}:{self.port}")
        threading.Thread(target=self.accept_peers, daemon=True).start()

    def accept_peers(self):
        while True:
            client_sock, addr = self.server_socket.accept()
            print(f"[EdgeToEdge] Connected by {addr}")
            self.peers.append(client_sock)
            threading.Thread(target=self.handle_client, args=(client_sock,), daemon=True).start()

    def handle_client(self, client_sock):
        while True:
            try:
                data = client_sock.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                print(f"[EdgeToEdge] Received: {message}")
                # Handle message or forward to other peers as needed
            except Exception as e:
                print(f"[EdgeToEdge] Error: {e}")
                break
        client_sock.close()

    def send_to_peer(self, peer_sock, message):
        try:
            data = json.dumps(message).encode()
            peer_sock.sendall(data)
            print(f"[EdgeToEdge] Sent message to peer")
        except Exception as e:
            print(f"[EdgeToEdge] Failed to send: {e}")
