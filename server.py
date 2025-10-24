from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}  # key = sid, value = {'x': int, 'y': int, 'name': str}

@app.route('/')
def index():
    return "Server is running!"

# When a player joins with their name
@socketio.on('join')
def handle_join(data):
    sid = request.sid
    name = data['name']
    players[sid] = {'x': 100, 'y': 100, 'name': name}
    emit('update_players', players, broadcast=True)
    print(f"{name} joined the game!")

# When a player disconnects
@socketio.on('disconnect')
def disconnect():
    sid = request.sid
    if sid in players:
        print(f"{players[sid]['name']} disconnected")
        del players[sid]
        emit('update_players', players, broadcast=True)

# When a player moves
@socketio.on('player_action')
def player_action(data):
    sid = request.sid
    if sid in players:
        players[sid]['x'] = data['x']
        players[sid]['y'] = data['y']
        emit('update_players', players, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
