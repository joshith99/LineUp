# Professor Availability and Token Queue System

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A lightweight, self-hosted real-time application to manage professor-student interactions using sockets.

## 🚀 Overview

Professors often face time constraints when meeting students for lab work, project discussions, or doubt clarification.  
This **self-hosted** system solves that by providing:

- **Real-time professor availability status**
- **Live student token queue**
- **Socket-based updates**
- **Separate professor and student interfaces**
- **Complete control over your data** - Host it yourself!

Built using **Flask-SocketIO**, **Python**, and **HTML/JS**. Designed to run on your own server, VPS, or local network.

---

## 🏠 Self-Hosted Benefits

- ✅ **Full data control** - Your data stays on your server
- ✅ **No third-party dependencies** - Run it anywhere
- ✅ **Customizable** - Modify to fit your needs
- ✅ **Privacy-first** - No external tracking
- ✅ **Cost-effective** - Run on cheap VPS or local machine
- ✅ **Offline-capable** - Works on local network without internet

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
- **Deployment:** Self-hosted on VPS, dedicated server, or local network
- **Database:** In-memory (can be extended to SQLite/PostgreSQL)

## 🧪 Quick Start

### 1. Clone this repo:
   ```bash
   git clone https://github.com/joshith99/LineUp.git
   cd LineUp
   ```

### 2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Run the server:
   ```bash
   python server.py
   ```

### 4. Access the interfaces:
   - **Students:** `http://YOUR_SERVER_IP:5000`
   - **Professor App:** Run `python professor_app.py` or use the compiled `.exe`

---

## 🌐 Deployment Options

### **Option 1: Local Network** (Easiest)
Perfect for classroom/office use:
1. Run server on your computer
2. Students connect via your local IP (e.g., `http://192.168.1.100:5000`)
3. No internet required!

### **Option 2: VPS/Cloud Server** (Recommended for Production)
Deploy on any VPS provider:
- **DigitalOcean** ($6/month)
- **Linode** ($5/month)
- **AWS/Azure/GCP** (Free tier available)
- **Your own server**

See [DEPLOYMENT.md](#) for detailed instructions.

### **Option 3: Docker** (Coming Soon)
```bash
docker-compose up
```

---

## 🔒 Security & Privacy

- ✅ No data collection or tracking
- ✅ All data stored locally on your server
- ✅ No external API calls
- ✅ Full control over access and permissions
- ⚠️ Remember to configure firewall and HTTPS for production use

---

## 📦 What You Get

- ✅ Complete source code (GPL v3 licensed)
- ✅ Self-hosted solution - own your data
- ✅ Easy deployment instructions
- ✅ Active development and community support
- ✅ No vendor lock-in
