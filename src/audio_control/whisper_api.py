import socket
import threading
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import warnings
import time

warnings.filterwarnings("ignore", category=UserWarning)

AUDIO_PORT = 12346
BUFFER_SIZE = 4096
TIMEOUT = 60

fs = 16000
seconds = 5  
alphabet = ['a','b','c','d','e','f','g','h']
numbers = ['1','2','3','4','5','6','7','8']

model = whisper.load_model("base")

class AudioServer:
    def __init__(self):
        self.server_socket = None
        self.running = False
        
    def record_audio(self):
        try:
            print("Recording...")
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=np.int16)
            sd.wait()  # Wait until recording is finished
            write("audio_file/output.wav", fs, myrecording)  # Save as WAV file
            print("end of recording")
            return True
        except Exception as e:
            print("Fail")
            return False

    def transcribe_audio(self):
        res = model.transcribe("audio_file/output.wav")
        transcript = res['text'].strip().lower()
        if not res:
            return None
        else:
            return (transcript)

    def extract_move_from_transcript(self, transcript):        
        letter = None
        num = None
        
        for char in transcript:
            if char in alphabet and letter is None:
                letter = char
            elif char in numbers and num is None:
                num = char
                
        if letter and num:
            move = letter + num
            print(f"Extracted move: {move}")
            return move
        
        miss_w = {
            'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h',
            'bee': 'b', 'see': 'c', 'dee': 'd', 'gee': 'g',
            'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8',
            'won': '1', 'to': '2', 'too': '2', 'tree': '3', 'free': '3', 'for': '4', 'ate': '8'
        }
        
        words = transcript.split()
        for w in words:
            if w in miss_w:
                if miss_w[w] in alphabet and letter is None:
                    letter = miss_w[w]
                elif miss_w[w] in numbers and num is None:
                    num = miss_w[w]
        
        if letter and num:
            move = letter.upper() + num
            print(f"Extracted move: {move}")
            return move
            
        return None

    def get_audio_move(self, max_attempts=10):
        for attempt in range(max_attempts):
            print(f"Attempt {attempt + 1}/{max_attempts}")
            
            if self.record_audio():
                transcript = self.transcribe_audio()
                if transcript:
                    move = self.extract_move_from_transcript(transcript)
                    if move:
                        return move
                    else:
                        print("Extract error")
                else:
                    print("Transcription error")
            else:
                print("Fail")
            
            if attempt < max_attempts - 1:
                time.sleep(1)
        return None

    def handle_client(self, client_socket, address):
        while True:
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break
            
            print(f"Received from {address}: {data}")
            
            parts = data.split('|')
            if len(parts) >= 2:
                command = parts[0]
                
                if command == '0':
                    move = self.get_audio_move()
                    move1 = move[0]
                    move = move1.upper() + move[1]
                    if move:
                        resp = f"5|{move}|"
                    else:
                        resp = "4| |"
                
                elif command == '1':
                    print("Move accepted!")
                    resp = "1|OK|"
                
                elif command == '4':
                    print("Invalid move! Please try again.")
                    resp = "4| |"
                
                else:
                    resp = "4| |"
                
                client_socket.sendall(resp.encode())
                print(f"Resp: {resp}")

        client_socket.close()
        print(f"Connection with {address} closed")

    def start_server(self):
        sd._terminate()
        sd._initialize()
        
        # Create audio_file directory if it doesn't exist
        import os
        if not os.path.exists("audio_file"):
            os.makedirs("audio_file")
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind(('localhost', AUDIO_PORT))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"Audio server started on localhost:{AUDIO_PORT}")
            print("Waiting for connections...")
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"Connection established with {address}")
                    
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"Error accepting connection: {e}")
                
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop_server()

    def stop_server(self):
        """Stop the audio server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Audio server stopped")

if __name__ == "__main__":
    server = AudioServer()
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop_server()