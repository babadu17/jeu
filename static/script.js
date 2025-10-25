const socket = io();
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const playerId = Math.random().toString(36).substr(2, 9);
const playerName = "Joueur_" + playerId.substring(0, 4);

socket.emit("join", { id: playerId, name: playerName });

let players = {};
let objects = [];

socket.on("update_game", (data) => {
    players = data.players;
    objects = data.objects;
    draw();
});

// 💀 Quand on est mangé
socket.on("eaten", (data) => {
    alert("💀 Tu as été mangé par " + data.by + " !");
});

// --- Déplacement souris ---
document.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    socket.emit("move", { id: playerId, x, y });
});

// --- Dessin ---
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // objets (points à ramasser)
    for (const obj of objects) {
        ctx.fillStyle = "orange";
        ctx.beginPath();
        ctx.arc(obj.x, obj.y, 8, 0, Math.PI * 2);
        ctx.fill();
    }

    // joueurs
    for (const id in players) {
        const p = players[id];
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = id === playerId ? "blue" : "green";
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = "black";
        ctx.font = "12px Arial";
        ctx.fillText(p.name + " (" + p.score + ")", p.x - 20, p.y - p.size - 10);
    }
}
