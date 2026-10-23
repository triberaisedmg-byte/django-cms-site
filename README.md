# TribeRaised Marketing Website (`django-cms-site`)

Official public marketing website for the **TribeRaised** ecosystem (`triberaised.com`), built with **Django 4.2 LTS** and **Django CMS 4**.

---

## 🛠️ Tech Stack & Architecture

- **Runtime**: Python 3.12
- **Framework**: Django 4.2 LTS / Django CMS 4.1
- **Database**: PostgreSQL 18 (`tr-profile-postgres` or local Docker PostgreSQL), with SQLite fallback for quick testing
- **WSGI / Server**: Gunicorn
- **Static Asset Serving**: WhiteNoise (with Brotli & Gzip compression)
- **Containerization**: Multi-stage production `Dockerfile` (non-root `appuser`) and `docker-compose.local.yml`
- **Testing**: `pytest`, `pytest-django`

---

## 🚀 Quick Start (Local CLI)

### 1. Prerequisites
Ensure Python 3.12 and PostgreSQL (or Docker) are installed on your machine.

### 2. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 3. Virtual Environment & Dependencies
Using `uv`:
```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements-dev.txt
```

Or using standard `venv` and `pip`:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 4. Database Migrations
Apply database migrations:
```bash
python manage.py migrate
```

*(Note: To use SQLite instead of PostgreSQL, set `USE_SQLITE=True` in `.env`)*

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver 0.0.0.0:8001
```

Visit:
- Marketing Site: [http://localhost:8001/](http://localhost:8001/)
- Admin Panel: [http://localhost:8001/admin/](http://localhost:8001/admin/)
- Health Check Probe: [http://localhost:8001/healthz](http://localhost:8001/healthz)

---

## 🐳 Docker Local Development

To launch the full stack (Django CMS + PostgreSQL 18 container) using Docker Compose:

```bash
docker compose -f docker-compose.local.yml up --build
```

The application will be accessible at [http://localhost:8001/](http://localhost:8001/).

---

## 🧪 Running Tests

Execute the test suite using `pytest`:

```bash
pytest
```

Or with coverage:
```bash
pytest --cov=apps --cov=config
```

---

## 📁 Project Structure

```
django-cms-site/
├── Dockerfile                  # Multi-stage production container definition
├── docker-compose.local.yml    # Local development container orchestration
├── .env.example                # Canonical environment template
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development and testing dependencies
├── pyproject.toml              # Project metadata & tool configs
├── manage.py                   # Django CLI entrypoint
├── config/                     # Core project configuration
│   ├── settings/
│   │   ├── base.py             # Shared settings & CMS configs
│   │   ├── local.py            # Development-specific settings
│   │   └── production.py       # Production & GCP Cloud Run hardening
│   ├── urls.py                 # Root routing (CMS, Admin, Healthz)
│   ├── wsgi.py                 # Gunicorn WSGI entrypoint
│   └── asgi.py                 # ASGI entrypoint
├── apps/
│   └── core/                   # System probes and common utilities
├── templates/
│   ├── base.html               # Main layout shell
│   └── cms/                    # CMS page templates
├── static/                     # Static assets (CSS, JS, images)
├── media/                      # Uploaded media assets
└── tests/                      # Automated test suite
```
