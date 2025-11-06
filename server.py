from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Application State
state = {
    'professor_status': 'Unavailable',  # Available, Busy, In Cabin, Unavailable
    'current_token': None,
    'queue': [],  # List of {id, name, type, timestamp}
    'token_counter': 1
}

# Routes
@app.route('/')
def student():
    """Student interface"""
    return render_template('student.html')

@app.route('/professor')
def professor():
    """Professor dashboard (web-based alternative)"""
    return render_template('professor.html')

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    """Send current state when client connects"""
    emit('state_update', state)
    print(f"Client connected at {datetime.now()}")

@socketio.on('request_token')
def handle_token_request(data):
    """Handle student token request"""
    token = {
        'id': state['token_counter'],
        'name': data.get('name', 'Anonymous'),
        'type': data.get('type', 'General'),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    state['queue'].append(token)
    state['token_counter'] += 1
    
    # Broadcast update to all clients
    socketio.emit('state_update', state)
    print(f"Token requested: {token}")

@socketio.on('update_status')
def handle_status_update(data):
    """Update professor status"""
    new_status = data.get('status')
    if new_status in ['Available', 'Busy', 'In Cabin', 'Unavailable']:
        state['professor_status'] = new_status
        socketio.emit('state_update', state)
        print(f"Status updated to: {new_status}")

@socketio.on('next_token')
def handle_next_token():
    """Move to next token in queue"""
    if state['queue']:
        state['current_token'] = state['queue'].pop(0)
        socketio.emit('state_update', state)
        print(f"Now serving: {state['current_token']}")
    else:
        state['current_token'] = None
        socketio.emit('state_update', state)
        print("Queue is empty")

@socketio.on('clear_current')
def handle_clear_current():
    """Clear current token"""
    state['current_token'] = None
    socketio.emit('state_update', state)
    print("Current token cleared")

@socketio.on('get_state')
def handle_get_state():
    """Send current state to requesting client"""
    emit('state_update', state)

if __name__ == '__main__':
    print("🚀 Server starting on http://localhost:5000")
    print("📱 Student interface: http://localhost:5000")
    print("👨‍🏫 Professor dashboard: http://localhost:5000/professor")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
