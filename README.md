# Pimtong Work Manager

A web application to manage Sales, Projects, and Services for Pimtong.
Features:
- **Work Orders**: Manage jobs (Sales, Project, Service).
- **Dashboard**: Visualize schedules and current status.
- **Telegram Bot**: Technicians can check tasks via `/today`.
- **AI Integration**: Quick add jobs using natural language.

## Setup

### Prerequisites
- Python 3.9+
- Docker (for PostgreSQL)

### Installation

1. **Start Database**:
   Make sure Docker is running, then start the database container:
   ```bash
   docker-compose up -d
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate on macOS/Linux
   source venv/bin/activate

   # Activate on Windows
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   - Rename `.env.example` to `.env` (or create one) and set your keys:
     - `DATABASE_URL`
     - `TELEGRAM_BOT_TOKEN`
     - `GOOGLE_API_KEY`

### Running the App

```bash
uvicorn app.main:app --reload --port 9000
```

Access the dashboard at: http://127.0.0.1:9000

## API Documentation

- Swagger UI: http://127.0.0.1:9000/docs
- ReDoc: http://127.0.0.1:9000/redoc

## Project Structure

- `app/main.py`: Entry point.
- `app/api`: API endpoints.
- `app/core`: Configuration, Database, Auth, AI, Telegram.
- `app/models`: SQLAlchemy models.
- `app/templates`: HTML templates (Jinja2 + Tailwind).
