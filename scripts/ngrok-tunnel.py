# Ngrok.py

import subprocess
import os
import time

# Funcție pentru a citi tokenul ngrok din fișier
def read_ngrok_token(file_path):
    with open(file_path, 'r') as f:
        token = f.read().strip()
    return token

# Funcție pentru a porni ngrok în fundal cu comanda specificată
def start_ngrok(token, label, local_port, log_file):
    command = f"ngrok authtoken {token} && ngrok tunnel --label edge={label} http://localhost:{local_port}"
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

# Montăm Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Calea către directorul de lucru
base_path = '/content/drive/My Drive/Host/ngrok'

# Calea către fișierul cu tokenul ngrok
token_file_path = os.path.join(base_path, 'ngrok.txt')

# Calea către fișierul în care vom scrie logurile ngrok
log_file_path = os.path.join(base_path, 'edge.txt')

# Citim tokenul ngrok din fișier
ngrok_token = read_ngrok_token(token_file_path)

# Pornim ngrok în fundal cu noua comandă
start_ngrok(ngrok_token, 'edghts_2iZKNtAUmzQkIzcEA09GynEGDDK', 5555, log_file_path)

# Așteptăm o scurtă perioadă de timp înainte de a continua
time.sleep(3)  # Așteaptă 3 secunde pentru a permite ngrok să înceapă în fundal

# Aici poți continua cu alte coduri
print("Ngrok Edge Started.")
