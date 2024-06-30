import os
import subprocess
import time
from datetime import datetime

# Function to stop an existing tmate session
def stop_tmate_session():
    try:
        subprocess.run('tmate -S /tmp/tmate.sock kill-session', shell=True, check=True)
        print('Old tmate session has been stopped.')
    except subprocess.CalledProcessError as e:
        print(f'Error stopping tmate session: {e}')

# Function to get the tmate SSH link and set the current directory in tmate session
def get_tmate_ssh_link_and_cd():
    # Stop any existing tmate session
    stop_tmate_session()

    # Wait for 2 seconds to ensure the old session has completely terminated
    time.sleep(2)

    # Start a new tmate session
    subprocess.run('tmate -S /tmp/tmate.sock new-session -d', shell=True, check=True)

    # Wait for 5 seconds for tmate to generate the link
    time.sleep(5)

    # Send the "cd /drive/MyDrive/Host" command to tmate session
    subprocess.run('tmate -S /tmp/tmate.sock send-keys "cd /drive/MyDrive/Host" C-m', shell=True)

    # Wait for 1 second to allow the command to execute in the session
    time.sleep(1)

    # Get the SSH link command
    result = subprocess.run('tmate -S /tmp/tmate.sock display -p "#{tmate_ssh}"', shell=True, stdout=subprocess.PIPE)
    tmate_ssh_link = result.stdout.decode().strip()

    return tmate_ssh_link

# Directory where tmate.txt files will be saved
tmate_dir = '/content/drive/MyDrive/Host/SSH'

# Function to ensure the directory exists or create it if it doesn't
def ensure_directory_exists(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        print(f'Error creating directory {directory}: {e}')

# Function to clear old tmate files from the directory
def clear_old_tmate_files(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f'Deleted old file: {file_path}')
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    except FileNotFoundError:
        print(f'Directory {directory} does not exist.')

# Ensure the directory exists or create it if it doesn't
ensure_directory_exists(tmate_dir)

# Check and delete old files in the SSH directory
clear_old_tmate_files(tmate_dir)

# Generate a unique file name using current date and time
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
tmate_txt_path = os.path.join(tmate_dir, f'tmate_{timestamp}.txt')

# Attempt to establish tmate connection
try:
    # Get the tmate SSH link and set the current directory in tmate session
    tmate_ssh_link = get_tmate_ssh_link_and_cd()

    # Write the SSH link to tmate.txt file
    with open(tmate_txt_path, 'w') as file:
        file.write(tmate_ssh_link)

    print(f'Saved SSH link to file: {tmate_txt_path}')

except subprocess.CalledProcessError as e:
    print(f'Error starting tmate: {e}')
except Exception as e:
    print(f'Unexpected error: {e}')
