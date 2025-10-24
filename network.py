import socketio

class Network:
    def __init__(self, server_url='http://localhost:5000'):
        self.sio = socketio.Client()
        self.sio.connect(server_url)
        self.players = {}

        @self.sio.event
        def connect():
            print("Connected to server!")

        @self.sio.event
        def disconnect():
            print("Disconnected from server!")

        @self.sio.event
        def update_players(data):
            self.players = data  # update positions for all players

    def join_game(self, name):
        self.sio.emit('join', {'name': name})

    def send_action(self, x, y):
        self.sio.emit('player_action', {'x': x, 'y': y})
