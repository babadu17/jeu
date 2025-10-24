from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random
import os

app = Flask(__name__)
socketio = SocketIO(app)

players = {}
objects = []

# Fonction pour créer des objets aléatoires
def spawn_objects():
    global objects
    objects = []
    for _ in range(5):
        objects.append({'id': random.randint(1000, 9999),
                        'x': random.randint(20, 580),
                        'y': random.randint(20, 380)})

spawn_objects()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_player')
def new_player(data):
    players[data['id']] = {
        'x': data['x'],
        'y': data['y'],
        'color': data['color'],
        'score': 0,
        'size': 15,  # taille initiale
        'sid': request.sid
    }
    emit('update_game', {'players': players, 'objects': objects}, broadcast=True)

@socketio.on('move')
def move(data):
    if data['id'] in players:
        p = players[data['id']]
        p['x'] = data['x']
        p['y'] = data['y']

        # Vérifier collision avec objets
        for obj in objects[:]:
            if abs(p['x'] - obj['x']) < p['size'] and abs(p['y'] - obj['y']) < p['size']:
                p['score'] += 1
                p['size'] += 2  # augmente la taille
                objects.remove(obj)
                socketio.start_background_task(spawn_object_delayed)

        emit('update_game', {'players': players, 'objects': objects}, broadcast=True)

def spawn_object_delayed():
    socketio.sleep(3)
    objects.append({'id': random.randint(1000, 9999),
                    'x': random.randint(20, 580),
                    'y': random.randint(20, 380)})
    emit('update_game', {'players': players, 'objects': objects}, broadcast=True)

@socketio.on('disconnect')
def disconnect_player():
    removed = False
    for pid in list(players):
        if players[pid].get('sid') == request.sid:
            del players[pid]
            removed = True
            break
    if removed:
        emit('update_game', {'players': players, 'objects': objects}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
