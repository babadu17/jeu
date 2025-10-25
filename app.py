from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random, time

app = Flask(__name__)
socketio = SocketIO(app)

CANVAS_W, CANVAS_H = 800, 600
players = {}
objects = []

PLAYER_MIN_SIZE = 10
PLAYER_MAX_SIZE = 80

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def spawn_object():
    obj = {"x": random.randint(20, CANVAS_W - 20), "y": random.randint(20, CANVAS_H - 20)}
    objects.append(obj)

def spawn_object_delayed(delay=3):
    time.sleep(delay)
    spawn_object()
    emit_game_update()

def emit_game_update():
    socketio.emit("update_game", {"players": players, "objects": objects}, broadcast=True)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def connect():
    print("Un joueur s'est connecté")

@socketio.on("disconnect")
def disconnect():
    sid = request.sid
    for pid, p in list(players.items()):
        if p.get("sid") == sid:
            del players[pid]
    emit_game_update()

@socketio.on("join")
def join(data):
    pid = data["id"]
    players[pid] = {
        "x": random.randint(0, CANVAS_W),
        "y": random.randint(0, CANVAS_H),
        "size": PLAYER_MIN_SIZE,
        "score": 0,
        "sid": request.sid,
        "name": data.get("name", f"Joueur {pid[:4]}")
    }
    emit_game_update()

@socketio.on("move")
def move(data):
    pid = data.get("id")
    if pid not in players:
        return

    p = players[pid]
    p["x"] = clamp(int(data["x"]), 0, CANVAS_W)
    p["y"] = clamp(int(data["y"]), 0, CANVAS_H)

    # Collision avec objets
    for obj in objects[:]:
        if abs(p["x"] - obj["x"]) < p["size"] and abs(p["y"] - obj["y"]) < p["size"]:
            p["score"] += 1
            p["size"] = clamp(p["size"] + 2, PLAYER_MIN_SIZE, PLAYER_MAX_SIZE)
            objects.remove(obj)
            socketio.start_background_task(spawn_object_delayed)

    # Collision entre joueurs
    eaten, eater = None, None
    for jid, other in list(players.items()):
        if jid == pid:
            continue
        dx = abs(p["x"] - other["x"])
        dy = abs(p["y"] - other["y"])
        if dx < (p["size"] + other["size"]) and dy < (p["size"] + other["size"]):
            if p["size"] > other["size"]:
                p["score"] += other["size"] // 2
                p["size"] += other["size"] // 2
                eaten, eater = jid, pid
            elif p["size"] < other["size"]:
                other["score"] += p["size"] // 2
                other["size"] += p["size"] // 2
                eaten, eater = pid, jid
            break

    if eaten and eaten in players:
        sid = players[eaten].get("sid")
        if sid:
            socketio.emit("eaten", {"by": players[eater]["name"]}, to=sid)
        del players[eaten]

    emit_game_update()

if __name__ == "__main__":
    for _ in range(5):
        spawn_object()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
