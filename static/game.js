const socket = io();

const playerId = Math.random().toString(36).substring(2, 10);
const playerColor = '#' + Math.floor(Math.random()*16777215).toString(16);
let x = Math.random() * 600;
let y = Math.random() * 400;
const speed = 10;

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let players = {};
let objects = [];

// Envoyer nouvel arrivant
socket.emit('new_player', {id: playerId, x, y, color: playerColor});

// Recevoir mise à jour complète
socket.on('update_game', (data) => {
    players = data.players;
    objects = data.objects;
});

// Déplacements clavier
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp') y -= speed;
    if (e.key === 'ArrowDown') y += speed;
    if (e.key === 'ArrowLeft') x -= speed;
    if (e.key === 'ArrowRight') x += speed;
    socket.emit('move', {id: playerId, x, y});
});

// Boucle de rendu
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dessiner objets
    ctx.fillStyle = 'gold';
    for (let obj of objects) {
        ctx.fillRect(obj.x, obj.y, 15, 15);
    }

    // Dessiner joueurs
    for (let id in players) {
        const p = players[id];
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
        ctx.fill();
        ctx.fillStyle = '#000';
        ctx.fillText(p.score, p.x - 5, p.y - p.size - 5); // score au-dessus
    }

    requestAnimationFrame(draw);
}

draw();
