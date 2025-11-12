// Connect to Socket.IO server
const socket = io();

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const themeText = document.getElementById('themeText');
const themeIcon = document.querySelector('.theme-toggle-icon');

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', currentTheme);
updateThemeButton(currentTheme);

themeToggle.addEventListener('click', () => {
    const theme = document.documentElement.getAttribute('data-theme');
    const newTheme = theme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeButton(newTheme);
});

function updateThemeButton(theme) {
    if (theme === 'dark') {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Light';
    } else {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Dark';
    }
}

// DOM Elements
const statusEl = document.getElementById('status');
const currentTokenEl = document.getElementById('current-token');
const queueCountEl = document.getElementById('queue-count');
const queueListEl = document.getElementById('queue-list');
const tokenForm = document.getElementById('token-form');

// Handle connection
socket.on('connect', () => {
    console.log('Connected to server');
    socket.emit('get_state');
});

// Handle state updates
socket.on('state_update', (state) => {
    updateStatus(state.professor_status);
    updateCurrentToken(state.current_token);
    updateQueue(state.queue);
});

// Update professor status
function updateStatus(status) {
    statusEl.textContent = status;
    statusEl.className = 'status-badge status-' + status.toLowerCase().replace(' ', '-');
}

// Update current token display
function updateCurrentToken(token) {
    if (token) {
        currentTokenEl.innerHTML = `
            <div class="token-id">Token #${token.id}</div>
            <div class="token-info">
                <strong>${token.name}</strong><br>
                ${token.type}
            </div>
        `;
    } else {
        currentTokenEl.innerHTML = '<p class="waiting">No one is being served</p>';
    }
}

// Update queue display
function updateQueue(queue) {
    queueCountEl.textContent = queue.length;
    
    if (queue.length === 0) {
        queueListEl.innerHTML = '<p class="empty-queue">Queue is empty</p>';
        return;
    }
    
    queueListEl.innerHTML = queue.map(token => `
        <div class="queue-item">
            <div class="queue-item-info">
                <div class="queue-item-name">${token.name}</div>
                <div class="queue-item-type">${token.type}</div>
            </div>
            <div class="queue-item-id">#${token.id}</div>
        </div>
    `).join('');
}

// Handle token request form submission
tokenForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value.trim();
    const type = document.getElementById('type').value;
    
    if (!name) {
        alert('Please enter your name');
        return;
    }
    
    // Send token request
    socket.emit('request_token', { name, type });
    
    // Reset form
    tokenForm.reset();
    
    // Show confirmation
    alert(`Token requested successfully!\nName: ${name}\nType: ${type}`);
});

// Handle disconnection
socket.on('disconnect', () => {
    console.log('Disconnected from server');
    statusEl.textContent = 'Disconnected';
    statusEl.className = 'status-badge status-unavailable';
});
