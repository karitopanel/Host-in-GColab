from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Funcție pentru a cere tokenul
def get_ngrok_token():
    token = input("Paste the ngrok token: ").strip()
    return token

# Funcție pentru a salva tokenul într-un fișier text
def save_token_to_file(token, file_path):
    with open(file_path, 'w') as f:
        f.write(token)
    print(f"Ngrok token was saved in: {file_path}")

# Montăm Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Definim calea către directorul de lucru
base_path = '/content/drive/My Drive/Host/ngrok'

# Verificăm dacă folderul există, altfel îl cream
if not os.path.exists(base_path):
    os.makedirs(base_path)

# Calea completă către fișierul în care vom salva tokenul
token_file_path = os.path.join(base_path, 'ngrok.txt')

# Cerem și salvăm tokenul
token = get_ngrok_token()
save_token_to_file(token, token_file_path)
