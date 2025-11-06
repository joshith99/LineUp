import tkinter as tk
from tkinter import ttk, messagebox
import socketio
import pystray
from PIL import Image, ImageDraw
import threading
import sys

class ProfessorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LineUp - Professor Control")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        # SocketIO client
        self.sio = socketio.Client()
        self.setup_socketio()
        
        # State
        self.state = {
            'professor_status': 'Unavailable',
            'current_token': None,
            'queue': []
        }
        
        # UI Setup
        self.setup_ui()
        
        # System tray
        self.tray_icon = None
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
        # Connect to server
        self.connect_to_server()
    
    def setup_socketio(self):
        """Setup SocketIO event handlers"""
        @self.sio.on('connect')
        def on_connect():
            print("Connected to server")
            self.sio.emit('get_state')
            self.update_connection_status(True)
        
        @self.sio.on('disconnect')
        def on_disconnect():
            print("Disconnected from server")
            self.update_connection_status(False)
        
        @self.sio.on('state_update')
        def on_state_update(data):
            self.state = data
            self.update_ui()
    
    def setup_ui(self):
        """Create the UI"""
        # Header
        header = tk.Frame(self.root, bg="#667eea", height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="🎓 LineUp", font=("Arial", 20, "bold"),
                        bg="#667eea", fg="white")
        title.pack(pady=20)
        
        # Main container
        main = tk.Frame(self.root, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Connection status
        self.conn_label = tk.Label(main, text="⚫ Disconnected", 
                                   font=("Arial", 10), fg="red")
        self.conn_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Status Section
        status_frame = tk.LabelFrame(main, text="Professor Status", 
                                    font=("Arial", 12, "bold"), padx=10, pady=10)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_var = tk.StringVar(value="Unavailable")
        statuses = ["Available", "Busy", "In Cabin", "Unavailable"]
        
        for status in statuses:
            tk.Radiobutton(status_frame, text=status, variable=self.status_var,
                          value=status, font=("Arial", 10),
                          command=self.update_status).pack(anchor=tk.W, pady=2)
        
        # Current Token Section
        current_frame = tk.LabelFrame(main, text="Currently Serving", 
                                     font=("Arial", 12, "bold"), padx=10, pady=10)
        current_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.current_label = tk.Label(current_frame, text="No one", 
                                     font=("Arial", 11), fg="#666")
        self.current_label.pack(pady=5)
        
        btn_frame = tk.Frame(current_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.next_btn = tk.Button(btn_frame, text="Next Token", 
                                 font=("Arial", 10, "bold"),
                                 bg="#10b981", fg="white", 
                                 command=self.next_token, height=2)
        self.next_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.clear_btn = tk.Button(btn_frame, text="Clear", 
                                  font=("Arial", 10, "bold"),
                                  bg="#ef4444", fg="white",
                                  command=self.clear_current, height=2)
        self.clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Queue Section
        queue_frame = tk.LabelFrame(main, text="Queue", 
                                   font=("Arial", 12, "bold"), padx=10, pady=10)
        queue_frame.pack(fill=tk.BOTH, expand=True)
        
        self.queue_label = tk.Label(queue_frame, text="Total: 0", 
                                   font=("Arial", 10, "bold"))
        self.queue_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Queue listbox with scrollbar
        list_frame = tk.Frame(queue_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.queue_listbox = tk.Listbox(list_frame, font=("Arial", 9),
                                       yscrollcommand=scrollbar.set)
        self.queue_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.queue_listbox.yview)
        
        # Minimize button
        tk.Button(main, text="Minimize to Tray", command=self.minimize_to_tray,
                 bg="#6b7280", fg="white", font=("Arial", 9)).pack(pady=(10, 0))
    
    def connect_to_server(self):
        """Connect to the server in a separate thread"""
        def connect():
            try:
                self.sio.connect('http://localhost:5000')
            except Exception as e:
                messagebox.showerror("Connection Error", 
                                   f"Failed to connect to server:\n{e}")
        
        thread = threading.Thread(target=connect, daemon=True)
        thread.start()
    
    def update_connection_status(self, connected):
        """Update connection status label"""
        if connected:
            self.conn_label.config(text="🟢 Connected", fg="green")
        else:
            self.conn_label.config(text="⚫ Disconnected", fg="red")
    
    def update_status(self):
        """Update professor status"""
        status = self.status_var.get()
        if self.sio.connected:
            self.sio.emit('update_status', {'status': status})
        else:
            messagebox.showwarning("Not Connected", 
                                 "Please connect to the server first")
    
    def next_token(self):
        """Call next token"""
        if self.sio.connected:
            self.sio.emit('next_token')
        else:
            messagebox.showwarning("Not Connected", 
                                 "Please connect to the server first")
    
    def clear_current(self):
        """Clear current token"""
        if self.sio.connected:
            self.sio.emit('clear_current')
        else:
            messagebox.showwarning("Not Connected", 
                                 "Please connect to the server first")
    
    def update_ui(self):
        """Update UI with current state"""
        # Update status
        self.status_var.set(self.state['professor_status'])
        
        # Update current token
        current = self.state.get('current_token')
        if current:
            self.current_label.config(
                text=f"#{current['id']} - {current['name']}\n{current['type']}",
                fg="#000"
            )
        else:
            self.current_label.config(text="No one", fg="#666")
        
        # Update queue
        queue = self.state.get('queue', [])
        self.queue_label.config(text=f"Total: {len(queue)}")
        
        self.queue_listbox.delete(0, tk.END)
        for token in queue:
            self.queue_listbox.insert(tk.END, 
                f"#{token['id']} - {token['name']} ({token['type']})")
    
    def create_tray_icon(self):
        """Create system tray icon"""
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='#667eea')
        draw = ImageDraw.Draw(image)
        draw.ellipse([16, 16, 48, 48], fill='white')
        
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Exit", self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("LineUp", image, "LineUp Professor", menu)
    
    def minimize_to_tray(self):
        """Minimize to system tray"""
        self.root.withdraw()
        if self.tray_icon is None:
            self.create_tray_icon()
            thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            thread.start()
    
    def show_window(self):
        """Show the window from tray"""
        self.root.deiconify()
        self.root.lift()
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
    
    def quit_app(self):
        """Quit the application"""
        if self.sio.connected:
            self.sio.disconnect()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        sys.exit()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ProfessorApp()
    app.run()
