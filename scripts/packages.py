# Instalarea pachetelor cerute
!apt-get install nano wget curl unzip python-is-python3 python3-pip tmate screen -y

# Instalarea și configurarea ngrok
!curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
!echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
!sudo apt update
!sudo apt install ngrok -y
!pip install pydrive
!curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash
!apt install npm -y
!npm install pm2 -g && pm2 install pm2-logrotate
!pip install flask flask-socketio flask-cors
!npm install -g localtunnel
