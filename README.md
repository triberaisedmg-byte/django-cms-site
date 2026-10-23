# TribeRaised Marketing Website (`django-cms-site`)

Official public marketing website for the **TribeRaised** ecosystem (`triberaised.com`), built with **Django 4.2 LTS** and **Django CMS 4**.

---

## 🛠️ Tech Stack & Architecture

- **Runtime**: Python 3.12
- **Framework**: Django 4.2 LTS / Django CMS 4.1
- **Database**: PostgreSQL 18 (`tr-profile-postgres` on shared `triberaised_tr-network` Docker network), with SQLite fallback for quick testing
- **WSGI / Server**: Gunicorn / Django Development Server
- **Static Asset Serving**: WhiteNoise (with Brotli & Gzip compression)
- **Containerization**: Multi-stage production `Dockerfile` (non-root `appuser`) and `docker-compose.local.yml`
- **Testing**: `pytest`, `pytest-django`

---

## 🐳 Quick Start: Docker Local Deployment (`deploy-local.sh`)

The TribeRaised marketing site integrates into the shared **TribeRaised dev Docker group** (`triberaised_tr-network`), connecting to the shared PostgreSQL 18 container (`tr-profile-postgres`) on port `8001` (to avoid collision with `tr-triberaised-web` on port `8000`).

### 1. Prerequisites
Ensure Docker is installed and running. For the full integrated developer experience, start the main TribeRaised stack:
```bash
# In /home/markgordon/Documents/GitHub/triberaised:
./deploy-local.sh
```

### 2. Deploy the Marketing Site
Run the local deployment orchestration script:
```bash
./deploy-local.sh
```
This script automatically:
1. Validates Docker daemon health.
2. Attaches to (or creates) the shared `triberaised_tr-network` bridge network.
3. Verifies `tr-profile-postgres` health and idempotently creates the `triberaised_cms` database if it does not yet exist.
4. Builds the `tr-django-cms` Docker container image.
5. Launches the container in detached mode and executes Django migrations.
6. Polls the `/healthz` readiness probe until HTTP 200 OK is returned, displaying stack summary URLs.

### 3. Accessing the Application
- **Marketing Site**: [http://localhost:8001/](http://localhost:8001/)
- **Django CMS Admin**: [http://localhost:8001/admin/](http://localhost:8001/admin/)
- **Health Check Probe**: [http://localhost:8001/healthz](http://localhost:8001/healthz)

### 4. Create an Admin Superuser
To create an administrative user for accessing the Django CMS toolbar and page tree:
```bash
docker compose -f docker-compose.local.yml exec web python manage.py createsuperuser
```

### 5. Common Docker Commands
```bash
# View live container logs
docker compose -f docker-compose.local.yml logs -f web

# Apply new database migrations
docker compose -f docker-compose.local.yml exec web python manage.py migrate

# Stop the marketing site container
docker compose -f docker-compose.local.yml down
```

---

## 📦 Standalone Docker Mode

If working exclusively on marketing templates or plugins without running the main TribeRaised backend stack, run the deployment script in standalone mode:
```bash
./deploy-local.sh --standalone
```
This launches an isolated PostgreSQL 18 container (`tr-cms-standalone-db`) via `docker-compose.standalone.yml` without depending on `triberaised_tr-network`.

To stop the standalone stack:
```bash
docker compose -f docker-compose.standalone.yml down
```

---

## 💻 Local Host CLI Development (Outside Docker)

### 1. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 2. Virtual Environment & Dependencies
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

### 3. Database Migrations
When running directly on the host with the shared PostgreSQL running:
```bash
python manage.py migrate
```
*(Tip: To develop with an in-memory SQLite database without PostgreSQL, set `USE_SQLITE=True` in `.env`)*

### 4. Run Development Server
```bash
python manage.py runserver 0.0.0.0:8001
```

---

## 🧪 Running Tests

Execute the automated test suite using `pytest`:

```bash
pytest
```

Or with test coverage:
```bash
pytest --cov=apps --cov=config
```

Linting and formatting verification:
```bash
flake8
black --check .
```

---

## 📁 Project Structure

```
django-cms-site/
├── deploy-local.sh             # Local Docker orchestration & readiness probe script
├── docker-compose.local.yml    # Integrated compose attached to triberaised_tr-network
├── docker-compose.standalone.yml # Standalone compose with isolated postgres container
├── Dockerfile                  # Multi-stage production container definition
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
