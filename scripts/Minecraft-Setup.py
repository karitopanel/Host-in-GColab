from google.colab import drive
drive.mount('/content/drive')

import subprocess
import os
import requests
from bs4 import BeautifulSoup
from ipywidgets import interact, Dropdown, Button, Output, Text

# Funcție pentru instalarea unui server Minecraft într-un director specific
def install_server(server_type, minecraft_version, version_url, output_widget):
    server_dir = f"/content/drive/MyDrive/Host/Server/{server_type} ({minecraft_version})"
    try:
        os.makedirs(server_dir, exist_ok=True)
        
        # Descarcă serverul Minecraft folosind linkul specificat
        download_command = f"wget {version_url} -O '{server_dir}/server.jar'"
        subprocess.run(download_command, shell=True, check=True)
        
        with output_widget:
            print(f"Serverul {server_type} {minecraft_version} a fost instalat în {server_dir}")
    except Exception as e:
        with output_widget:
            print(f"Eroare în timpul instalării serverului {server_type} {minecraft_version}: {str(e)}")

# Funcție pentru a obține linkul de descărcare pentru Vanilla de la mcversions.net
def get_vanilla_url(minecraft_version):
    try:
        url = f"https://mcversions.net/download/{minecraft_version}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        download_link = soup.find('a', string='Server Download').get('href')
        return download_link
    except Exception as e:
        print(f"Eroare la obținerea linkului pentru Vanilla {minecraft_version}: {str(e)}")
        return None

# Funcție pentru a obține linkul de descărcare pentru Paper de la API-ul PaperMC
def get_paper_url(minecraft_version):
    try:
        url = f"https://api.papermc.io/v2/projects/paper/versions/{minecraft_version}/builds/{minecraft_version}/downloads/paper-{minecraft_version}.jar"
        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            raise Exception(f"Nu s-a putut obține linkul pentru Paper {minecraft_version}. Cod status: {response.status_code}")
    except Exception as e:
        print(f"Eroare la obținerea linkului pentru Paper {minecraft_version}: {str(e)}")
        return None

# Funcție pentru a obține linkul de descărcare pentru Purpur de la API-ul Purpur
def get_purpur_url(minecraft_version):
    try:
        url = f"https://purpur.pl3x.net/api/v1/purpur/{minecraft_version}/latest/download"
        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            raise Exception(f"Nu s-a putut obține linkul pentru Purpur {minecraft_version}. Cod status: {response.status_code}")
    except Exception as e:
        print(f"Eroare la obținerea linkului pentru Purpur {minecraft_version}: {str(e)}")
        return None

# Definirea meniului pentru selecția serverului Minecraft
def minecraft_menu():
    # Definirea opțiunilor pentru serverele Minecraft
    minecraft_versions = {
        "Vanilla (1.8 - 1.21)": ["1.8", "1.9", "1.10", "1.11", "1.12", "1.13", "1.14", "1.15", "1.16", "1.17", "1.18", "1.19", "1.20", "1.21"],
        "Paper (1.8.9 - 1.20.1)": ["1.8.8", "1.9.4", "1.10.2", "1.11.2", "1.12.2", "1.13.2", "1.14.4", "1.15.2", "1.16.5", "1.17.1", "1.18.1", "1.19.4", "1.20.1", "1.21"],
        "Purpur (1.16.5 - 1.20.1)": ["1.16.5", "1.17.1", "1.18.1", "1.19.4", "1.20.1"]
    }
    
    # Widget-uri pentru selecția tipului de server, versiunii și introducerea linkului custom
    server_type_dropdown = Dropdown(options=list(minecraft_versions.keys()), description='Selectează serverul:')
    minecraft_version_dropdown = Dropdown(options=minecraft_versions["Vanilla (1.8 - 1.21)"], description='Selectează versiunea:')
    custom_url_text = Text(description='Paste the link:', placeholder='https://url-server.jar')
    
    # Output pentru afișarea rezultatului instalării
    output = Output()
    
    # Funcție pentru actualizarea versiunilor disponibile în funcție de tipul de server selectat
    def update_versions(change):
        selected_server_type = change['new']
        minecraft_version_dropdown.options = minecraft_versions[selected_server_type]
    
    server_type_dropdown.observe(update_versions, names='value')
    
    # Funcție pentru instalarea serverului la apăsarea butonului
    def on_button_click(b):
        with output:
            server_type = server_type_dropdown.value
            minecraft_version = minecraft_version_dropdown.value
            if custom_url_text.value.strip():
                version_url = custom_url_text.value.strip()
            else:
                if server_type == "Vanilla (1.8 - 1.21)":
                    version_url = get_vanilla_url(minecraft_version)
                elif server_type == "Paper (1.8.9 - 1.20.1)":
                    version_url = get_paper_url(minecraft_version)
                elif server_type == "Purpur (1.16.5 - 1.20.1)":
                    version_url = get_purpur_url(minecraft_version)
                else:
                    raise ValueError(f"Tipul serverului '{server_type}' nu este suportat.")
            
            if version_url:
                install_server(server_type, minecraft_version, version_url, output)
    
    # Buton pentru a iniția instalarea serverului
    install_button = Button(description='Instalează', button_style='success')
    install_button.on_click(on_button_click)
    
    # Afișare widget-uri și output
    display(server_type_dropdown)
    display(minecraft_version_dropdown)
    display(custom_url_text)
    display(install_button)
    display(output)

# Rulează meniul pentru selecția serverului Minecraft
minecraft_menu()
