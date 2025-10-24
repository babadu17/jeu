let score = 0;
let pointsPerClick = 1;

const scoreElement = document.getElementById("score");
const perClickElement = document.getElementById("perClick");
const clickBtn = document.getElementById("clickBtn");

const upgrade1Btn = document.getElementById("buyUpgrade1");
const upgrade2Btn = document.getElementById("buyUpgrade2");

let upgrade1Price = 50;
let upgrade2Price = 200;

// Clic normal
clickBtn.addEventListener("click", () => {
    score += pointsPerClick;
    updateDisplay();
});

// Achat amélioration 1 (+1 point par clic)
upgrade1Btn.addEventListener("click", () => {
    if (score >= upgrade1Price) {
        score -= upgrade1Price;
        pointsPerClick += 1;
        upgrade1Price = Math.floor(upgrade1Price * 1.5); // augmente le prix à chaque achat
        document.getElementById("upgrade1Price").textContent = upgrade1Price;
        updateDisplay();
    } else {
        alert("Pas assez de points !");
    }
});

// Achat amélioration 2 (+5 points par clic)
upgrade2Btn.addEventListener("click", () => {
    if (score >= upgrade2Price) {
        score -= upgrade2Price;
        pointsPerClick += 5;
        upgrade2Price = Math.floor(upgrade2Price * 1.5);
        document.getElementById("upgrade2Price").textContent = upgrade2Price;
        updateDisplay();
    } else {
        alert("Pas assez de points !");
    }
});

function updateDisplay() {
    scoreElement.textContent = score;
    perClickElement.textContent = pointsPerClick;
}