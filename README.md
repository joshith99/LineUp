# Professor Availability and Token Queue System

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A lightweight real-time application to manage professor-student interactions using sockets.

## 🚀 Overview

Professors often face time constraints when meeting students for lab work, project discussions, or doubt clarification.  
This system solves that by providing:

- **Real-time professor availability status**
- **Live student token queue**
- **Socket-based updates**
- **Separate professor and student interfaces**

Built using **Flask-SocketIO**, **Python**, and **HTML/JS**, and designed to be hosted on a VPS.

---

## 🧠 Features

- Professor can update their **status** (`Available`, `Busy`, `In Cabin`, etc.)
- Students can **request a token** with their **name** and **type**
- Everyone can see:
  - Current professor status
  - **Current token** being served
  - **Total tokens** in queue
- Real-time synchronization via WebSockets

---

## 🏗️ Architecture

```
Professor Client (Python CLI/Tray)
        │
        ▼
[ Flask-SocketIO Server ]
        ▲
        │
        ▼
Student Web Interface (HTML + JS)
```

---

## ⚙️ Tech Stack

- **Backend:** Flask + Flask-SocketIO  
- **Frontend:** HTML, CSS, JS (Socket.IO client)
- **Language:** Python 3.10+
- **Deployment:** VPS or local network

## 🧪 Quick Start

1. Clone this repo:
   ```bash
   git clone https://github.com/joshith99/LineUp.git
   cd LineUp
   ```

2. Install dependencies:
   ```bash
   pip install flask flask-socketio
   ```

3. Run the server:
   ```bash
   python3 server.py
   ```

4. Open the student UI in a browser:
   ```
   http://localhost:5000
   ```

5. Run the professor client in another terminal:
   ```bash
   python3 professor_client.py
   ```
