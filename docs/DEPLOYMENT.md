# RWA Deployment Guide

This guide covers deploying the RWA platform in various environments.

## Prerequisites

### System Requirements

- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 20GB minimum for application + database
- **OS**: Linux (Ubuntu 22.04 LTS recommended), Windows Server 2019+, or macOS

### Software Requirements

- Python 3.11 or 3.12
- Node.js 20 LTS
- PostgreSQL 15+ with TimescaleDB extension
- Git

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/khaaliswooden-max/rwa.git
cd rwa
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Database Setup

```bash
# Create database (PostgreSQL)
createdb rwa_dev

# Enable TimescaleDB extension
psql rwa_dev -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

# Configure environment
cp env.example .env
# Edit .env with your database credentials

# Initialize database
python scripts/init_db.py --sample-data
```

### 4. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 5. Run Development Servers

```bash
# Terminal 1: Backend
python -m uvicorn api.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

Access:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Production Deployment

### Option 1: Docker Compose (Recommended)

#### Prerequisites
- Docker Engine 24+
- Docker Compose v2

#### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: timescale/timescaledb:latest-pg15
    environment:
      POSTGRES_DB: rwa
      POSTGRES_USER: rwa_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  api:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://rwa_user:${DB_PASSWORD}@db:5432/rwa
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - APP_ENV=production
      - DEBUG=false
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - api
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - api
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
```

#### Dockerfile (Backend)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run with uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Deploy

```bash
# Set environment variables
export DB_PASSWORD=your-secure-password
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret

# Start services
docker-compose up -d

# Initialize database
docker-compose exec api python scripts/init_db.py
```

---

### Option 2: Manual Server Deployment

#### 1. Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql-15 postgresql-contrib \
    nginx certbot python3-certbot-nginx \
    nodejs npm

# Install TimescaleDB
sudo apt install -y timescaledb-2-postgresql-15
sudo timescaledb-tune
sudo systemctl restart postgresql
```

#### 2. Create Database

```bash
sudo -u postgres createuser rwa_user -P
sudo -u postgres createdb rwa -O rwa_user
sudo -u postgres psql rwa -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

#### 3. Deploy Application

```bash
# Create application user
sudo useradd -m -s /bin/bash rwa
sudo -u rwa -i

# Clone and setup
git clone https://github.com/khaaliswooden-max/rwa.git
cd rwa
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp env.example .env
nano .env  # Edit configuration

# Initialize database
python scripts/init_db.py
```

#### 4. Setup Systemd Service

```ini
# /etc/systemd/system/rwa-api.service
[Unit]
Description=RWA API Server
After=network.target postgresql.service

[Service]
User=rwa
Group=rwa
WorkingDirectory=/home/rwa/rwa
Environment="PATH=/home/rwa/rwa/.venv/bin"
ExecStart=/home/rwa/rwa/.venv/bin/uvicorn api.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable rwa-api
sudo systemctl start rwa-api
```

#### 5. Configure Nginx

```nginx
# /etc/nginx/sites-available/rwa
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Frontend
    location / {
        root /home/rwa/rwa/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/rwa /etc/nginx/sites-enabled/
sudo certbot --nginx -d your-domain.com
sudo systemctl reload nginx
```

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `SECRET_KEY` | Yes | Application secret key |
| `JWT_SECRET_KEY` | Yes | JWT signing key |
| `APP_ENV` | No | Environment (development/production) |
| `DEBUG` | No | Debug mode (true/false) |
| `FRONTEND_URL` | No | Frontend URL for CORS |

### Security Checklist

- [ ] Change all default passwords
- [ ] Use strong, unique secret keys
- [ ] Enable HTTPS
- [ ] Configure firewall (allow only 80, 443, 22)
- [ ] Set up automated backups
- [ ] Enable database SSL
- [ ] Review rate limiting settings
- [ ] Set up log monitoring

---

## Maintenance

### Database Backups

```bash
# Manual backup
pg_dump rwa > backup_$(date +%Y%m%d).sql

# Automated daily backup (cron)
0 2 * * * pg_dump rwa | gzip > /backups/rwa_$(date +\%Y\%m\%d).sql.gz
```

### Updates

```bash
cd /home/rwa/rwa
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart rwa-api
```

### Logs

```bash
# API logs
journalctl -u rwa-api -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## Troubleshooting

### API Won't Start

1. Check logs: `journalctl -u rwa-api`
2. Verify database connection: `psql $DATABASE_URL -c "SELECT 1"`
3. Check environment variables

### Database Connection Issues

1. Verify PostgreSQL is running: `systemctl status postgresql`
2. Check connection string format
3. Verify user permissions

### Frontend 404 Errors

1. Ensure frontend is built: `cd frontend && npm run build`
2. Verify nginx root path
3. Check `try_files` directive

---

## Support

For deployment issues:
- Open a [GitHub Issue](https://github.com/khaaliswooden-max/rwa/issues)
- Email: support@visionblox.io

