import socket
import threading
import time
import queue


class Server:
    def __init__(self, host='localhost', port=4321):
        self.host = host
        self.port = port
        self.socket = None
        self.client_socket = None
        self.client_address = None
        self.running = False
        self.message_queue = queue.Queue()
        self.response_queue = queue.Queue()
        
    def start(self):
        """Démarre le serveur"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.running = True
            
            print(f"Serveur démarré sur {self.host}:{self.port}")
            print("En attente de connexions...")
            
            # Accepter une connexion
            self.client_socket, self.client_address = self.socket.accept()
            print(f"Connexion établie avec {self.client_address}")
            
            # Démarrer le thread de réception
            receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            receive_thread.start()
                    
        except Exception as e:
            print(f"Erreur serveur: {e}")
            self.stop()
    
    def _receive_messages(self):
        """Thread pour recevoir les messages du client"""
        try:
            while self.running and self.client_socket:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                print(f"Message reçu du client: {data}")
                self.message_queue.put(data)
                
        except socket.error as e:
            print(f"Erreur de réception: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()
    
    def accept_and_respond(self, timeout=60):
        """Attend un message du client et retourne le message reçu (string)"""
        try:
            message = self.message_queue.get(timeout=timeout)
            print(f"Message récupéré de la file: {message}")
            
            # Retourner le message tel quel (string), pas une liste
            return message.strip()
            
        except queue.Empty:
            print("Timeout: Aucun message reçu")
            return None
        except Exception as e:
            print(f"Erreur lors de la réception: {e}")
            return None
    
    def send_response(self, response):
        """Envoie une réponse au client"""
        try:
            if self.client_socket:
                self.client_socket.send(response.encode('utf-8'))
                print(f"Réponse envoyée au client: {response}")
                return True
            else:
                print("Aucune connexion client active")
                return False
        except socket.error as e:
            print(f"Erreur lors de l'envoi: {e}")
            return False
    
    def stop(self):
        """Arrête le serveur"""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        if self.socket:
            self.socket.close()
        print("Serveur arrêté")

class Client:
    def __init__(self, host='localhost', port=4321):
        self.host = host
        self.port = port
        self.socket = None
        self.timeout = 60  # Timeout de 60 secondes
        self.connected = False
        
    def connect(self):
        """Établit la connexion avec le serveur"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connecté au serveur {self.host}:{self.port}")
            return True
        except socket.error as e:
            print(f"Erreur de connexion: {e}")
            self.connected = False
            return False
    
    def send_request(self, message):
        """Envoie une requête au serveur et attend la réponse"""
        if not self.connected or not self.socket:
            print("Pas de connexion établie")
            if not self.connect():
                return None
            
        try:
            # Envoyer la requête
            print(f"Envoi de la requête: {message}")
            self.socket.send(message.encode('utf-8'))
            
            # Attendre la réponse avec timeout de 60 secondes
            print("Attente de la réponse (timeout: 60s)...")
            start_time = time.time()
            
            response = self.socket.recv(1024).decode('utf-8')
            end_time = time.time()
            
            print(f"Réponse reçue en {end_time - start_time:.2f}s: {response}")
            
            # Retourner la réponse telle quelle (string), pas une liste
            return response.strip()
            
        except socket.timeout:
            print("Timeout: Aucune réponse reçue dans les 60 secondes")
            return None
        except socket.error as e:
            print(f"Erreur lors de l'envoi/réception: {e}")
            self.connected = False
            return None
    
    def disconnect(self):
        """Ferme la connexion"""
        if self.socket:
            self.socket.close()
            self.socket = None
            self.connected = False
            print("Connexion fermée")
    
    def is_connected(self):
        """Vérifie si la connexion est active"""
        return self.connected and self.socket is not None


if __name__ == "__main__":
    client = Client()
    client.connect()