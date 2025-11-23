// Variables que vienen de Django
let attempts = djangoData.attempts;
const level = djangoData.level;
const csrfToken = djangoData.csrfToken;

const cards = document.querySelectorAll('.card');
let flippedCards = [];
let matchedPairs = 0;
let score = 0;
const gameStartTime = Date.now();

// Sonidos
const victorySound = new Audio('/static/memory_game/sounds/levelComplete.mp3');
const loseSound = new Audio('/static/memory_game/sounds/derrota.mp3');
const gameMusic = document.getElementById('bg-music');

victorySound.preload = 'auto';
loseSound.preload = 'auto';
gameMusic.preload = 'auto';
gameMusic.volume = 0.2;

// Iniciar música de fondo al cargar
document.addEventListener('DOMContentLoaded', () => {
    gameMusic.play().catch(e => console.log('Autoplay bloqueado, espera interacción del usuario.'));
});

// Elementos de UI
const scoreDisplay = document.getElementById('score');
const attemptsDisplay = document.getElementById('attempts');
const modal = document.getElementById('endModal');
const modalTitle = document.getElementById('modal-title');
const modalStats = document.getElementById('modal-stats');
const retryBtn = document.getElementById('retryBtn');
const menuBtn = document.getElementById('menuBtn');

// Función fin de juego
function endGame(win) {
    const elapsedSeconds = Math.floor((Date.now() - gameStartTime) / 1000);

    // Detener música de fondo
    gameMusic.pause();
    gameMusic.currentTime = 0;

    // Mostrar modal
    modal.style.display = 'flex';
    modalTitle.textContent = win ? '¡Ganaste! 🏆' : '¡Perdiste! 😢';
    modalStats.innerHTML = `
        Intentos restantes: ${attempts} <br>
        Puntaje: ${score} <br>
        Parejas encontradas: ${matchedPairs}/${cards.length/2} <br>
        Tiempo: ${elapsedSeconds} segundos
    `;

    // Sonido de resultado
    if (win) {
        victorySound.currentTime = 0;
        victorySound.play();
    } else {
        loseSound.currentTime = 0;
        loseSound.play();
    }

    // Guardar estadísticas
    fetch('/save-stats/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
    },
    body: JSON.stringify({
        level: level,
        score: score,
        attempts: attempts,
        pairs: matchedPairs,
        duration: elapsedSeconds,
        win: win
    })
    })
}
// Botones del modal
retryBtn.onclick = () => window.location.reload();
menuBtn.onclick = () => window.location.href = '/select-level/';

// Lógica de cartas
cards.forEach(card => {
    card.addEventListener('click', () => {
        if (flippedCards.length < 2 && !card.classList.contains('flipped') && attempts > 0) {
            card.classList.add('flipped');
            flippedCards.push(card);

            if (flippedCards.length === 2) {
                const [first, second] = flippedCards;

                if (first.dataset.card === second.dataset.card) {
                    matchedPairs++;
                    score += 100;
                    scoreDisplay.textContent = score;
                    flippedCards = [];

                    if (matchedPairs === cards.length / 2) {
                        setTimeout(() => endGame(true), 500);
                    }
                } else {
                    attempts--;
                    attemptsDisplay.textContent = attempts;
                    setTimeout(() => {
                        first.classList.remove('flipped');
                        second.classList.remove('flipped');
                        flippedCards = [];
                    }, 800);
                    if (attempts === 0) {
                        setTimeout(() => endGame(false), 500);
                    }
                }
            }
        }
    });
});
