from google.colab import drive
drive.mount('/content/drive')

import os

# Calea către directorul principal al Google Drive montat în Colab
drive_path = '/content/drive/My Drive/'

# Numele noului folder pe care vrei să-l creezi
folder_name = 'Host'

# Calea completă către noul folder
folder_path = os.path.join(drive_path, folder_name)

# Creează folderul dacă nu există deja
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f'Folder "{folder_name}" was created in Google Drive.')
else:
    print(f'Folder "{folder_name}" already exist in Google Drive.')
