import subprocess
import os
from ipywidgets import interact, Dropdown, Button, Output

# Funcție pentru instalarea unei versiuni Java într-un director specific
def install_java(version_url, java_version, output_widget):
    java_dir = f"/content/drive/MyDrive/Host/Java/{java_version}"
    try:
        os.makedirs(java_dir, exist_ok=True)
        
        # Descarcă arhiva Java
        download_command = f"curl -fsSL {version_url} -o java.tar.gz"
        subprocess.run(download_command, shell=True, check=True)
        
        # Extrage arhiva Java în directorul specific
        extract_command = f"tar -xf java.tar.gz -C '{java_dir}' --strip-components=1"
        subprocess.run(extract_command, shell=True, check=True)
        
        # Șterge arhiva descărcată
        os.remove("java.tar.gz")
        
        with output_widget:
            print(f"Versiunea Java {java_version} a fost instalată în {java_dir}")
    except Exception as e:
        with output_widget:
            print(f"Eroare în timpul instalării Java {java_version}: {str(e)}")

# Definirea meniului Java cu widget-uri interactive
def java_menu():
    # Definirea opțiunilor pentru versiunile Java
    java_versions = {
        "Java 8": "https://github.com/karitopanel/WebFile-Host/releases/download/Java/OpenJDK8U-jdk_x64_linux_hotspot_8u412b08.tar.gz",
        "Java 11": "https://github.com/Adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz",
        "Java 17": "https://github.com/Adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz",
        "Java 21": "https://download.oracle.com/java/21/latest/jdk-21_linux-aarch64_bin.tar.gz"
    }
    
    # Widget pentru selecția versiunii Java
    java_dropdown = Dropdown(options=list(java_versions.keys()), description='Selectează Java:')
    
    # Output pentru afișarea rezultatului instalării
    output = Output()
    
    # Funcție pentru instalarea versiunii selectate
    def on_button_click(b):
        output.clear_output()
        java_version = java_dropdown.value
        version_url = java_versions[java_version]
        install_java(version_url, java_version, output)
    
    # Buton pentru a iniția instalarea
    install_button = Button(description='Instalează', button_style='success')
    install_button.on_click(on_button_click)
    
    # Afișare widget-uri și output
    display(java_dropdown)
    display(install_button)
    display(output)

# Rulează meniul Java
java_menu()
