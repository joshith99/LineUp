# Contribution and Future Enhancements

## ✅ Current MVP
- Real-time status and queue using Flask-SocketIO
- Professor CLI for status updates and next-token control
- Student web interface to request tokens and view live data

---

## 🚀 Planned Features

### 1. Smart Queue System (ETA Prediction)
- Predict waiting times based on average meeting duration.
- Display "Your turn in ~10 minutes" for students.

### 2. Time-Slot Scheduler
- Professors can pre-define slots (e.g., 2–4 PM).
- Students can book specific slots.

### 3. Presence Detection
- Auto-set professor status based on Wi-Fi or system activity.

### 4. Batch Queries
- Allow group tokens for similar topics (e.g., "Project Debugging").

### 5. Chat + Notifications
- In-app chat between professor and students.
- Browser/desktop notifications when turn arrives.

### 6. Analytics Dashboard
- Professor insights: total students, average session time, etc.

### 7. Public Display Board
- QR code or web widget showing live status outside cabin.

---

## 🧩 Tech Improvements
- Migrate to persistent DB (SQLite → PostgreSQL)
- JWT-based authentication
- Containerized deployment with Docker
- Logging & error tracing with `structlog` or `loguru`

---

## 💬 Contribution Guidelines
1. Fork this repository.
2. Work in a feature branch.
3. Ensure code passes local tests.
4. Open a pull request with a clear description.

---
