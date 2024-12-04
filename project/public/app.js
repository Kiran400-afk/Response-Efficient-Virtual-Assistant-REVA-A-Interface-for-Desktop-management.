const socket = io();
let isListening = false;
let recognition;

// Setup Web Speech API
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
} else {
    alert('Speech recognition is not supported in this browser.');
}

// DOM Elements
const listenButton = document.getElementById('listenButton');
const statusText = document.getElementById('status');
const responseText = document.getElementById('responseText');
const canvas = document.getElementById('voiceVisualization');
const ctx = canvas.getContext('2d');

// Setup canvas
function setupCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}

// Initialize visualization
setupCanvas();
window.addEventListener('resize', setupCanvas);

// Voice visualization
function drawVisualization() {
    if (!isListening) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const bars = 20;
    const barWidth = (canvas.width / bars) - 2;

    for (let i = 0; i < bars; i++) {
        const height = isListening ? Math.random() * canvas.height * 0.8 : 0;
        const x = i * (barWidth + 2) + 1;
        const y = canvas.height - height;

        ctx.fillStyle = '#007AFF';
        ctx.fillRect(x, y, barWidth, height);
    }

    if (isListening) {
        requestAnimationFrame(drawVisualization);
    }
}

// Button click handler
listenButton.addEventListener('click', () => {
    if (!isListening) {
        startListening();
    } else {
        stopListening();
    }
});

// Start listening
function startListening() {
    isListening = true;
    listenButton.classList.add('active');
    statusText.textContent = 'Listening...';
    drawVisualization();
    
    if (recognition) {
        recognition.start();
    }
}

// Stop listening
function stopListening() {
    isListening = false;
    listenButton.classList.remove('active');
    statusText.textContent = 'Click to start listening';
    
    if (recognition) {
        recognition.stop();
    }
}

// Recognition handlers
if (recognition) {
    recognition.onresult = (event) => {
        const command = event.results[0][0].transcript;
        socket.emit('command', command);
        responseText.textContent = `You said: ${command}`;
    };

    recognition.onend = () => {
        stopListening();
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        stopListening();
        statusText.textContent = 'Error occurred. Try again.';
    };
}

// Socket.IO handlers
socket.on('response', (response) => {
    responseText.textContent = response;
});

socket.on('error', (error) => {
    responseText.textContent = 'Error: ' + error;
});