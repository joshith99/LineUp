# LineUp v0.1.0 - Initial Release

🎉 First public release of LineUp - Professor Availability and Token Queue System!

## ✨ Features

### 🔧 Backend Server
- Real-time Flask-SocketIO server
- WebSocket-based live updates
- Token queue management
- Professor status tracking

### 📱 Student Web Interface
- Beautiful, responsive design
- Real-time status display
- Token request form with name and query type
- Live queue visualization
- Auto-updating when changes occur

### 👨‍🏫 Professor Desktop Application
- **Standalone Windows executable** (no Python required!)
- Tkinter GUI with modern design
- System tray support with full controls
- Update status (Available/Busy/In Cabin/Unavailable)
- Next token button
- Clear current token button
- Real-time queue monitoring
- Desktop notifications
- Minimize to tray functionality
- Control everything from system tray menu

## 📦 Installation

### Server Setup
```bash
pip install -r requirements.txt
python server.py
```

### Professor App
- **Windows**: Just run `LineUpProfessor.exe` (included in release assets)
- **Python**: `python professor_app.py`

### Students
- Open browser: `http://YOUR_SERVER_IP:5000`

## 🚀 Quick Start

See [QUICKSTART.md](https://github.com/joshith99/LineUp/blob/main/QUICKSTART.md) for detailed instructions.

## 📋 Requirements

- **Server**: Python 3.10+, Flask, Flask-SocketIO
- **Professor App (exe)**: Windows 10/11 (no additional requirements)
- **Students**: Any modern web browser

## 🐛 Known Issues

None reported yet!

## 📝 Changelog

See [CHANGELOG.md](https://github.com/joshith99/LineUp/blob/main/CHANGELOG.md) for detailed changes.

---

**Full Changelog**: https://github.com/joshith99/LineUp/commits/v0.1.0
