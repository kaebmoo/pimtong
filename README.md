# Pimtong Work Manager

A comprehensive web application designed to streamline Sales, Projects, and Service operations for **Pimtong**.

## 🚀 Key Features

### 🛠 Work Order Management
- **Job Types**: Manage Sales, Projects, and Service jobs.
- **Status Workflow**: Track jobs from Pending -> Assigned -> In Progress -> Completed.
- **Detailed Logs**: Automatic history tracking (Who changed what, when).
- **Product Info**: Record Product Type, Model, and Serial Number for every job.
- **Printable Job Sheets**: Generate professional A4 job sheets with one click.

### 📊 Dashboard & Analytics
- **Overview**: Real-time stats on job statuses and technician availability.
- **Reports**: Exportable reports (Excel/CSV) and visual charts for performance analysis.
- **Calendar**: Drag-and-drop calendar view for scheduling.

### 👥 Team & Project Management
- **Teams**: Group technicians into teams for easier assignment.
- **Projects**: Group multiple jobs under a single Project entity.
- **Technician Filters**: Filter jobs by specific technicians or teams.

### 🤖 Smart Integrations
- **AI-Powered**: Quick-add jobs using natural language commands.
- **Telegram Bot**: Technicians can check their daily schedule via `/today`.

## 🛠 Tech Stack

- **Backend**: Python (FastAPI)
- **Frontend**: Server-Side Rendering (Jinja2) + Tailwind CSS + Alpine.js
- **Database**: PostgreSQL (Production) / SQLite (Dev)
- **Maps**: Leaflet.js + OpenStreetMap

## 📦 Setup & Installation

### Prerequisites
- Python 3.9+
- Docker (optional, for local Postgres)

### Local Development

1. **Clone & Install**
   ```bash
   git clone https://github.com/pimtong/pimtong.git
   cd pimtong
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   Rename `.env.example` to `.env` and configure your Database URL and API Keys.

3. **Run Application**
   ```bash
   uvicorn app.main:app --reload --port 9000
   ```
   Visit: http://127.0.0.1:9000

## ☁️ Deployment (Vercel)

This project is configured for deployment on Vercel.

### Database Migration on Vercel
Vercel does not automatically run migration scripts. After every deployment that involves database schema changes:

1. Deploy your code.
2. Visit this URL **once** to apply database migrations:
   ```
   https://<your-app-url>.vercel.app/setup/migrate
   ```
3. You should see `"Migration V2 applied successfully"`.

### 🤖 Telegram Bot (Webhook Setup)

Since Vercel is serverless, the bot cannot run in "Polling Mode" (run_bot.py). You must set up a **Webhook**.

1. **Deploy to Vercel**: Ensure your app is live (e.g., `https://pimtong-app.vercel.app`).
2. **Set Webhook**: Open your browser or terminal and run this command:
   ```bash
   # Replace <YOUR_TOKEN> and <VERCEL_URL>
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://<VERCEL_URL>/api/webhook/telegram"
   ```
   *Expected Result*: `{"ok":true, "result":true, "description":"Webhook was set"}`

3. **Verify**:
   - Send `/start` to your bot. It should respond immediately.
   - Run `python run_bot.py` locally to auto-switch back to Local Mode (Polling) for testing.

## 📁 Project Structure

- `app/main.py`: Application entry point.
- `app/api`: REST API endpoints (`jobs.py`, `users.py`, etc.).
- `app/core`: Core logic (Config, DB, Auth, AI).
- `app/models`: SQLAlchemy Database Models.
- `app/templates`: HTML Templates (Jinja2).
- `app/static`: Static assets (CSS, JS).

---
**Pimtong WM** - Internal Tool
