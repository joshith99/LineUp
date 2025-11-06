# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Flask-SocketIO backend server (`server.py`)
  - Real-time professor status management
  - Token queue system
  - WebSocket-based live updates
- Student web interface
  - Real-time status display
  - Token request form
  - Live queue visualization
  - Responsive design
- Professor desktop application (`professor_app.py`)
  - Tkinter GUI with system tray support
  - Status update controls
  - Next token/Clear buttons
  - Real-time queue monitoring
  - Minimize to tray functionality
- Project structure (templates/, static/ directories)
- Python dependencies (requirements.txt)
- .gitignore file
- QUICKSTART.md with setup and usage instructions

### Changed

### Deprecated

### Removed

### Fixed
- SocketIO connection issues in professor app
  - Added websocket-client dependency
  - Improved connection error handling
  - Added multiple transport options (websocket, polling)
- Server configuration for better stability
  - Changed async_mode to 'threading'
  - Added allow_unsafe_werkzeug flag
  - Disabled debug mode for production readiness

### Security

### Deprecated

### Removed

### Fixed

### Security

---

## [0.1.0] - 2025-11-06

### Added
- Initial repository setup
- Git repository initialized and pushed to GitHub
- Basic project structure created
