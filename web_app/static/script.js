document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    document.getElementById('reset-btn').addEventListener('click', resetScan);
});

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

// Drag & Drop
dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#fff';
    dropZone.style.background = 'rgba(50, 50, 50, 0.5)';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255, 255, 255, 0.2)';
    dropZone.style.background = 'rgba(20, 20, 20, 0.5)';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255, 255, 255, 0.2)';
    dropZone.style.background = 'rgba(20, 20, 20, 0.5)';
    handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
    if (!file) return;

    // Reset UI
    const resultArea = document.getElementById('result-area');
    resultArea.style.display = 'none';

    // Show Preview
    const reader = new FileReader();
    reader.onload = function (e) {
        const preview = document.getElementById('image-preview');
        preview.src = e.target.result;
        document.getElementById('preview-area').style.display = 'flex';

        // Start Scan Animation
        const scanLine = document.createElement('div');
        scanLine.className = 'scanner-line';
        scanLine.style.display = 'block';
        document.getElementById('preview-area').appendChild(scanLine);

        playSound('scan');
    }
    reader.readAsDataURL(file);

    // Send to Backend
    const formData = new FormData();
    formData.append('file', file);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Stop Scan Animation
            const scanLine = document.querySelector('.scanner-line');
            if (scanLine) scanLine.remove();

            showResult(data);
        })
        .catch(err => {
            console.error(err);
            alert('System Error: Connection Lost');
        });
}

function showResult(data) {
    const resultArea = document.getElementById('result-area');
    const resultLabel = document.getElementById('result-label');
    const confidenceText = document.getElementById('confidence-text');
    const gaugeFill = document.getElementById('gauge-fill');
    const sysMsg = document.getElementById('system-msg');
    const resetBtn = document.getElementById('reset-btn');

    resultArea.style.display = 'block';

    if (data.error) {
        resultLabel.innerText = "ERROR";
        resultLabel.className = 'fake-verdict'; // Red for error
        sysMsg.innerText = data.error.toUpperCase();
        confidenceText.innerText = "ERR";
        gaugeFill.style.stroke = '#ff0000';
        gaugeFill.style.strokeDashoffset = 125; // 0%
        playSound('alarm');
        resetBtn.style.display = 'inline-block';
        return;
    }

    // Update Text
    resultLabel.innerText = data.label;
    confidenceText.innerText = Math.round(data.confidence) + "%";

    // Update Gauge (Arc Length 125 approx)
    const percentage = data.confidence / 100;
    const offset = 125 - (125 * percentage);
    gaugeFill.style.strokeDashoffset = offset;

    // Color Coding & Sound
    if (data.label === 'REAL') {
        resultLabel.className = 'real-verdict';
        gaugeFill.style.stroke = '#ffffff'; // White
        sysMsg.innerText = "AUTHENTIC PATTERNS DETECTED";
        playSound('success');
    } else {
        resultLabel.className = 'fake-verdict';
        gaugeFill.style.stroke = '#888888'; // Gray
        sysMsg.innerText = "SYNTHETIC ARTIFACTS FOUND";
        playSound('alarm');
    }

    // Show Neural View
    document.getElementById('neural-view').src = data.neural_view;

    resetBtn.style.display = 'inline-block';
    addToHistory(data.label, data.confidence);
}

function resetScan() {
    document.getElementById('result-area').style.display = 'none';
    document.getElementById('preview-area').style.display = 'none';
    document.getElementById('file-input').value = '';
    document.getElementById('image-preview').src = '';
    document.getElementById('reset-btn').style.display = 'none';
}

// Audio System (Synthesized)
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playSound(type) {
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    if (type === 'scan') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.5);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.5);
    }
    else if (type === 'success') {
        osc.type = 'square';
        osc.frequency.setValueAtTime(400, audioCtx.currentTime);
        osc.frequency.setValueAtTime(600, audioCtx.currentTime + 0.1);
        gain.gain.value = 0.1;
        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
    }
    else if (type === 'alarm') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(200, audioCtx.currentTime);
        osc.frequency.linearRampToValueAtTime(100, audioCtx.currentTime + 0.3);
        gain.gain.value = 0.2;
        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
    }
}

// LocalStorage History
function addToHistory(label, confidence) {
    const historyList = document.getElementById('history-list');
    const item = document.createElement('li');
    item.className = 'history-item';

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    item.innerHTML = `[${time}] <strong>${label}</strong> (${Math.round(confidence)}%)`;

    historyList.prepend(item);

    // Limit to 10
    if (historyList.children.length > 10) historyList.lastChild.remove();
}

function loadHistory() {
    // Just a placeholder for session history
}
