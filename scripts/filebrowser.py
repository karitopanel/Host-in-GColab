# filebrowser.py


from google.colab import drive
import os

# Montează Google Drive
drive.mount('/content/drive')

# Crează folderul 'Host' în Google Drive dacă nu există deja
host_folder = '/content/drive/My Drive/Host'
if not os.path.exists(host_folder):
    os.makedirs(host_folder)

# Instalează FileBrowser și pornește-l pe portul 5555 în fundal
!nohup filebrowser -r /content/drive/My\ Drive/Host --port 5555 &

# Așteaptă 5 secunde pentru a permite FileBrowser să înceapă în fundal
import time
time.sleep(5) 

# Verifică dacă FileBrowser rulează corect
!ps aux | grep filebrowser
