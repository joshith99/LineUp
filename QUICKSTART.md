# Quick Start Guide - Self-Hosted Setup

## 🏠 Running Your Self-Hosted LineUp Server

### Prerequisites
- Python 3.10 or higher
- A server/computer to host (VPS, dedicated server, or local machine)
- Network access for students to connect

---

## 🚀 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python server.py
```

The server will start on `http://0.0.0.0:5000` (accessible from network)

### 3. Access Interfaces

**For Students:**
- **Local Network**: `http://YOUR_LOCAL_IP:5000` (e.g., `http://192.168.1.100:5000`)
- **Public Server**: `http://YOUR_DOMAIN_OR_IP:5000`
- **Same Machine**: `http://localhost:5000`

**For Professor:**
- **Desktop App**: Run `python professor_app.py`
- **Or use compiled .exe** from releases (Windows only)

**Option A: Run the Executable (Recommended - No Python needed!)**
- Simply double-click: `dist/LineUpProfessor.exe`
- No installation or Python required!

**Option B: Run from Python**
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

## 🌐 Network Access (Self-Hosted Setup)

### Local Network Deployment

To allow students to access from other devices on the same network:

1. **Find your server's IP address:**
   - **Windows**: `ipconfig` (look for IPv4 Address)
   - **Linux/Mac**: `ifconfig` or `ip addr`

2. **Configure firewall:**
   - Allow incoming connections on port 5000
   - **Windows**: `netsh advfirewall firewall add rule name="LineUp" dir=in action=allow protocol=TCP localport=5000`
   - **Linux**: `sudo ufw allow 5000/tcp`

3. **Students access via:**
   - `http://YOUR_SERVER_IP:5000`
   - Example: `http://192.168.1.100:5000`

### VPS/Public Server Deployment

1. **Set up your VPS** (DigitalOcean, Linode, AWS, etc.)

2. **Install dependencies** on the server:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install -r requirements.txt
   ```

3. **Run with production server** (recommended):
   ```bash
   # Install gunicorn
   pip3 install gunicorn
   
   # Run with gunicorn
   gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 server:app
   ```

4. **Set up as system service** (auto-start on boot):
   ```bash
   # Create systemd service file
   sudo nano /etc/systemd/system/lineup.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=LineUp Queue System
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/LineUp
   ExecStart=/usr/bin/python3 server.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl enable lineup
   sudo systemctl start lineup
   ```

5. **Configure domain (optional):**
   - Point your domain to server IP
   - Set up Nginx as reverse proxy
   - Add SSL certificate (Let's Encrypt)

### Security Recommendations

- ✅ Use HTTPS in production (Let's Encrypt free SSL)
- ✅ Configure firewall properly
- ✅ Keep server updated
- ✅ Use strong passwords if adding authentication
- ✅ Regular backups of any persistent data

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

The professor app is already compiled as an executable in `dist/LineUpProfessor.exe`

To rebuild it yourself:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name LineUpProfessor professor_app.py
```

Or use the build script:
```bash
build_exe.bat
```

The .exe will be in the `dist/` folder and can be distributed to professors without requiring Python installation.
