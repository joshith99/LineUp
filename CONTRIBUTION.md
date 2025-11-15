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

## 🔐 Authentication (Auth)

Why: When LineUp is exposed beyond a trusted local network, it's important to restrict who can change professor state and access administrative features.

What to implement:
- Simple username/password login for the professor web UI (configurable via environment variable or admin setup flow).
- JWT-based tokens for API/WebSocket authentication so clients (professor apps) can prove identity.
- Role-based checks: `professor` vs `student` vs `admin` for sensitive actions (e.g., `next_token`, `clear_current`, editing timeslots).

Implementation notes:
- Use `Flask-Login` or a minimal custom auth layer for session-based web UI. For API/WebSocket, issue short-lived JWTs after login.
- Store user credentials hashed (e.g., `bcrypt`) if local user DB is used. Consider external providers (OAuth) as an option.
- Secure WebSocket connections by validating JWT on socket connect (check token during `connect` event).
- Add configuration options for enabling/disabling auth for quick local deployments.

Estimated effort: Medium (2–4 hours) for basic username/password + JWT flow.

---

## 🗓️ Time-slot Scheduler / Appointments

Why: Allowing professors to define fixed slots reduces walk-ins and supports appointment-based workflows.

What to implement:
- Professor UI to create, edit, and remove time-slots (date, start, end, capacity, label).
- Student booking flow with conflict detection and confirmation.
- Integration with queue: booked students can be inserted into the queue at scheduled times or handled separately.

Implementation notes:
- Model a `timeslot` entity with fields: `id, professor_id, start_ts, end_ts, capacity, booked_count, metadata`.
- For the MVP, store timeslots in the same persistent DB as tokens (SQLite). Use server-side checks to prevent double-booking.
- Add a small calendar-style view in the professor web UI (minimal, using a simple list is fine for v0.2).
- Notify booked students (in-app/browser) when their slot is approaching.

Estimated effort: Medium (3–6 hours) for basic scheduling + UI.

---

## 🗄️ Persistence / Database

Why: In-memory queues are simple but lose state on server restarts and do not provide history or analytics.

What to implement:
- Add a lightweight persistence layer (start with SQLite). Tables: `tokens`, `timeslots`, `users`, `events` (audit log).
- Ensure atomic operations when moving tokens from `queue` → `current_token` → `served`.
- Provide migration path to PostgreSQL for production deployments.

Implementation notes:
- Use the built-in `sqlite3` for minimal dependency projects or `SQLAlchemy` for a more portable ORM approach.
- On server start, load pending tokens into memory or operate directly against the DB for canonical state (latter simplifies multi-process scaling).
- Create simple stored fields for `created_at`, `served_at`, `duration` to compute analytics and ETA.

Estimated effort: Medium (2–4 hours) for core schema + migration helpers.

---

## 🧑‍🏫 Professor Web Interface (Admin UI)

Why: A richer web-based admin UI gives professors access to advanced configuration, reports, timeslot management, and remote control without the need for a desktop app.

What to implement:
- A `/professor` web dashboard (protected behind auth) with:
	- Status controls (Available/Busy/In Cabin/Unavailable)
	- Next/Clear token buttons
	- Timeslot management
	- Session statistics (served count, avg duration)
	- Live queue editing (reorder/cancel entries)
- Responsive design so it can be used on a tablet or phone.

Implementation notes:
- Reuse existing Socket.IO events for real-time updates and actions.
- Create REST endpoints for timeslot CRUD and settings.
- For quick delivery, use server-side templating (Jinja2) and progressive enhancement; no heavy SPA required for v0.2.

Estimated effort: Medium (3–6 hours) for a functional admin UI.

---

## 🔄 Inbuilt Update System (Auto-update)

Why: Professors should be able to update desktop clients or server components easily, especially in environments where end-users aren't technical.

What to implement:
- A simple self-update mechanism for the professor desktop app and an optional server-side update notifier.
- For the desktop app (Windows `.exe`): host releases on GitHub Releases; the app periodically checks the GitHub release API for a newer version and downloads/releases a new installer or `.exe`.
- For the server: a webhook or admin-triggered update script that can pull the latest release and perform a controlled restart.

Implementation notes:
- Desktop: implement an update-check endpoint that compares local app version (baked into the exe) with remote release tag; download and prompt user to install. Use atomic replacement and backup of previous exe.
- Server: provide a `./update.sh` (or PowerShell) script that validates release signatures, pulls the release assets, stops the service, replaces binaries, runs migrations, and restarts. Prefer manual approval for production.
- Security: Sign releases when possible and verify checksums to prevent supply-chain issues.

Estimated effort: Medium (3–6 hours) for a basic GitHub-based auto-update flow.

---

## How contributors can help

- Pick an item above and open an issue describing a proposed approach.
- For database work: provide migration scripts and tests that verify queue persistence across restarts.
- For timeslot and admin UI: provide UX mockups and small incremental PRs (start with REST endpoints, then wire the UI).
- For auth and updates: highlight security considerations in your PR and include tests/validation.

If you want, I can open starter issues for each of these features and include `good first issue` labels and acceptance criteria.

