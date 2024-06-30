import os
import subprocess
import threading
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

server_process = None
current_server = None

# Funcție pentru a porni LocalTunnel și a salva link-ul generat
def start_localtunnel():
    try:
        proc = subprocess.Popen(
            ['lt', '--port', '5000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in iter(proc.stdout.readline, ''):
            if 'url:' in line:
                url = line.split(' ')[-1].strip()
                with open('/content/drive/MyDrive/Host/LocalTunnel/link.txt', 'w') as f:
                    f.write(url)
                break
    except Exception as e:
        print(f"Error starting LocalTunnel: {e}")

@app.route('/')
def serve_static_index():
    return render_template_string(index_html)

def run_flask():
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=False, allow_unsafe_werkzeug=True)

index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minecraft Server Panel</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- CSS styling -->
    <style>
        body {
            background-color: #343a40;
            color: #fff;
        }
        .container {
            margin-top: 50px;
        }
        .card {
            background-color: #212529;
            border-color: #343a40;
            margin-bottom: 20px;
        }
        .card-title, .card-text, .btn, .form-control, .form-control:disabled {
            color: #fff;
            background-color: #343a40;
            border-color: #343a40;
        }
        .btn-primary, .btn-success, .btn-danger {
            background-color: #0069d9;
            border-color: #0069d9;
        }
        .btn-success {
            background-color: #28a745;
            border-color: #28a745;
        }
        .btn-danger {
            background-color: #dc3545;
            border-color: #dc3545;
        }
        .console {
            height: 400px;
            overflow-y: scroll;
            background-color: #000;
            padding: 10px;
            border: 1px solid #343a40;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Minecraft Server Control Panel</h5>
                <div class="form-group">
                    <label for="serverList">Available Servers</label>
                    <select id="serverList" class="form-control">
                        <option value="" disabled selected>Select a server</option>
                    </select>
                </div>
                <button id="startBtn" class="btn btn-success">Start</button>
                <button id="stopBtn" class="btn btn-danger">Stop</button>
                <hr>
                <div class="console" id="consoleOutput"></div>
                <div class="form-group">
                    <input type="text" id="consoleInput" class="form-control" placeholder="Enter command">
                </div>
                <button id="sendBtn" class="btn btn-primary">Send Command</button>
            </div>
        </div>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Current Server</h5>
                <p id="currentServer">None</p>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script>
        const socket = io();

        function fetchServers() {
            $.get('/servers', function(data) {
                const serverList = $('#serverList');
                serverList.empty();
                serverList.append('<option value="" disabled selected>Select a server</option>');
                data.forEach(function(server) {
                    serverList.append(`<option value="${server}">${server}</option>`);
                });
            });
        }

        function updateStatus() {
            $.get('/status', function(data) {
                $('#currentServer').text(data.current_server || 'None');
            });
        }

        $(document).ready(function() {
            fetchServers();
            updateStatus();

            $('#startBtn').click(function() {
                const serverName = $('#serverList').val();
                if (!serverName) {
                    alert('Please select a server');
                    return;
                }

                $.post('/start', JSON.stringify({ server_name: serverName }), function(response) {
                    alert(response.message);
                    updateStatus();
                }).fail(function(xhr) {
                    alert(xhr.responseJSON.error);
                });
            });

            $('#stopBtn').click(function() {
                $.post('/stop', function(response) {
                    alert(response.message);
                    updateStatus();
                }).fail(function(xhr) {
                    alert(xhr.responseJSON.error);
                });
            });

            $('#sendBtn').click(function() {
                const command = $('#consoleInput').val();
                if (command) {
                    socket.emit('send_command', { command });
                    $('#consoleInput').val('');
                }
            });

            socket.on('console_output', function(data) {
                $('#consoleOutput').append(`<div>${data.output}</div>`);
                $('#consoleOutput').scrollTop($('#consoleOutput')[0].scrollHeight);
            });
        });
    </script>
</body>
</html>
'''

def start_flask_and_localtunnel():
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Start LocalTunnel
    start_localtunnel()

if __name__ == '__main__':
    # Start Flask and LocalTunnel in background
    start_flask_and_localtunnel()
