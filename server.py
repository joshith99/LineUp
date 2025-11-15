from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import os

# MongoDB helpers (optional)
from db_mongo import connect, list_timeslots, create_timeslot, book_timeslot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Connect to MongoDB if available
try:
    connect()
    MONGO_ENABLED = True
except Exception:
    MONGO_ENABLED = False

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


# Timeslot REST API (MongoDB-backed if available)
@app.route('/api/timeslots', methods=['GET'])
def api_list_timeslots():
    if not MONGO_ENABLED:
        return jsonify({'error': 'MongoDB not enabled'}), 500
    docs = list_timeslots()
    # Serialize ObjectId and datetimes simply
    def s(d):
        d = dict(d)
        d['id'] = str(d.pop('_id'))
        d['start_ts'] = d['start_ts'].isoformat() if hasattr(d.get('start_ts'), 'isoformat') else d.get('start_ts')
        d['end_ts'] = d['end_ts'].isoformat() if hasattr(d.get('end_ts'), 'isoformat') else d.get('end_ts')
        return d
    return jsonify([s(x) for x in docs])


@app.route('/api/timeslots', methods=['POST'])
def api_create_timeslot():
    if not MONGO_ENABLED:
        return jsonify({'error': 'MongoDB not enabled'}), 500
    data = request.get_json() or {}
    try:
        # Expect ISO8601 strings for start/end
        from dateutil import parser
        start = parser.isoparse(data['start_ts'])
        end = parser.isoparse(data['end_ts'])
    except Exception:
        return jsonify({'error': 'Invalid or missing start_ts/end_ts (ISO format)'}), 400
    capacity = int(data.get('capacity', 1))
    label = data.get('label')
    t = create_timeslot(start, end, capacity=capacity, label=label)
    # Notify clients
    socketio.emit('timeslot_update', {'action': 'created', 'timeslot': {'id': str(t['_id']), 'start_ts': start.isoformat(), 'end_ts': end.isoformat(), 'capacity': capacity, 'label': label}})
    return jsonify({'id': str(t['_id'])}), 201


@app.route('/api/timeslots/<timeslot_id>/book', methods=['POST'])
def api_book_timeslot(timeslot_id):
    if not MONGO_ENABLED:
        return jsonify({'error': 'MongoDB not enabled'}), 500
    data = request.get_json() or {}
    name = data.get('name')
    contact = data.get('contact')
    if not name:
        return jsonify({'error': 'Missing name'}), 400
    try:
        booking = book_timeslot(timeslot_id, name, contact)
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 409
    # Notify clients
    b = dict(booking)
    b['id'] = str(b.pop('_id'))
    b['timeslot_id'] = str(b['timeslot_id'])
    socketio.emit('booking_update', {'action': 'created', 'booking': b})
    return jsonify({'id': b['id']}), 201

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
