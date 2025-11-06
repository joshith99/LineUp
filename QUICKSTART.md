# Quick Start Guide

## 🚀 Running the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python server.py
```

The server will start on `http://localhost:5000`

### 3. Access Interfaces

**For Students:**
- Open browser and go to: `http://localhost:5000`
- Or on mobile/other devices: `http://YOUR_IP:5000`

**For Professor:**
- Run the desktop app:
  ```bash
  python professor_app.py
  ```
- Or use web interface: `http://localhost:5000/professor`

## 📱 Using the System

### Student Interface
1. View professor's current status
2. See who's being served now
3. Check queue length
4. Request a token by entering:
   - Your name
   - Query type (Doubt/Project/Lab/Assignment/Other)

### Professor App
1. Update your status (Available/Busy/In Cabin/Unavailable)
2. Click "Next Token" to serve the next student
3. Click "Clear" to finish with current student
4. View live queue
5. Minimize to system tray to run in background

## 🌐 Network Access

To allow students to access from other devices on the same network:

1. Find your IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Linux/Mac: `ifconfig` or `ip addr`

2. Students access: `http://YOUR_IP:5000`

3. Make sure firewall allows port 5000

## 🛠️ Troubleshooting

**Server won't start:**
- Check if port 5000 is already in use
- Try: `python server.py` with administrator privileges

**Professor app won't connect:**
- Make sure server is running first
- Check the connection status indicator

**Students can't connect:**
- Verify firewall settings
- Make sure all devices are on the same network
- Try accessing via IP address instead of localhost

## 📦 Creating Executable (.exe)

To package the professor app as a standalone .exe:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name LineUpProfessor professor_app.py
```

The .exe will be in the `dist/` folder.
