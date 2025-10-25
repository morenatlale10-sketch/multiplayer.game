import json
import os
from network import Network

CONFIG_FILE = "Local_Multiplayer.json"

# Ask once if local or render
if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
    choice = input("Run local or render? ").strip().lower()
    if choice not in ["local", "render"]:
        print("Invalid choice! Defaulting to local.")
        choice = "local"
    with open(CONFIG_FILE, "w") as f:
        json.dump(choice, f)
else:
    with open(CONFIG_FILE, "r") as f:
        choice = json.load(f)

# Setup network URL
if choice == "local":
    server_url = "http://127.0.0.1:5050"
else:
    server_url = "https://multiplayer-game-k939.onrender.com"

# Create network instance
network = Network(server_url=server_url)
