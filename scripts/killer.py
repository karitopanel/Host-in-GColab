import os
import subprocess
from ipywidgets import interact, Dropdown, Button

# Funcție pentru a opri sesiunea Tmate
def stop_tmate_session():
    try:
        subprocess.run('tmate -S /tmp/tmate.sock kill-session', shell=True, check=True)
        print('Sesiunea Tmate veche a fost oprită.')
    except subprocess.CalledProcessError as e:
        print(f'Eroare la oprirea sesiunii Tmate: {e}')

# Funcție pentru a opri sesiunea Screen
def stop_screen_session():
    try:
        subprocess.run('screen -X -S session_name quit', shell=True, check=True)
        print('Sesiunea Screen veche a fost oprită.')
    except subprocess.CalledProcessError as e:
        print(f'Eroare la oprirea sesiunii Screen: {e}')

# Funcție pentru a opri sesiunea FileBrowser
def stop_filebrowser_session():
    try:
        subprocess.run('killall filebrowser', shell=True, check=True)
        print('Sesiunea FileBrowser veche a fost oprită.')
    except subprocess.CalledProcessError as e:
        print(f'Eroare la oprirea sesiunii FileBrowser: {e}')

# Funcția pentru a selecta și opri o sesiune
def stop_session(session_type):
    if session_type == 'Tmate':
        stop_tmate_session()
    elif session_type == 'Screen':
        stop_screen_session()
    elif session_type == 'FileBrowser':
        stop_filebrowser_session()

# Definirea meniului interactiv
def session_menu():
    session_dropdown = Dropdown(options=['Tmate', 'Screen', 'FileBrowser'], description='Selectează sesiunea:')
    stop_button = Button(description='Oprește sesiunea', button_style='danger')

    def on_button_click(b):
        selected_session = session_dropdown.value
        stop_session(selected_session)

    stop_button.on_click(on_button_click)

    # Afișare widget-uri
    display(session_dropdown)
    display(stop_button)

# Rulează meniul interactiv
session_menu()
