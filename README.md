# E-Commerce Application with Full Observability Stack

A complete e-commerce web application built with Flask, featuring comprehensive observability through the three pillars: **Metrics**, **Logs**, and **Traces**.

## 🎯 Features

### Application Features
- 🛒 **Shopping Cart System** - Add/remove products, manage quantities
- 👤 **User Authentication** - Registration, login/logout, session management
- 🛡️ **Admin Dashboard** - Product management (CRUD operations), user management, order tracking
- 📊 **Business Analytics** - Sales statistics, user activity tracking
- 💾 **SQLite Database** - Lightweight, file-based data storage
- 📱 **Responsive UI** - Modern, mobile-friendly interface

### Observability Features (Three Pillars)
- 📊 **Metrics (Prometheus)** - HTTP request metrics, business KPIs, performance monitoring
- 📝 **Logs (Loki)** - Structured JSON logging with request tracking, emoji-enhanced readability
- 🔍 **Traces (Tempo)** - Distributed tracing with OpenTelemetry, request flow visualization
- 📈 **Visualization (Grafana)** - Unified dashboards, real-time monitoring, log exploration

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Flask Application                        │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐   │
│  │  Routes  │  │ Services │  │  OpenTelemetry Tracing │   │
│  └──────────┘  └──────────┘  └────────────────────────┘   │
│       │              │                    │                 │
│  ┌────▼──────────────▼────────────────────▼────────┐       │
│  │            SQLite Database                       │       │
│  └──────────────────────────────────────────────────┘       │
│                      │                                       │
│         Exports: /metrics endpoint                          │
│                  app_json.log file                          │
│                  OTLP traces                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────────────┐
         │             │                     │
    ┌────▼────┐   ┌────▼─────┐   ┌─────────▼────┐
    │Prometheus│   │ Promtail │   │ OTLP Receiver│
    │(Metrics) │   │  (Logs)  │   │   (Traces)   │
    └────┬────┘   └────┬─────┘   └──────┬───────┘
         │             │                 │
         │        ┌────▼────┐       ┌────▼────┐
         │        │  Loki   │       │  Tempo  │
         │        │ (Store) │       │ (Store) │
         │        └────┬────┘       └────┬────┘
         │             │                 │
         └─────────────┼─────────────────┘
                       │
                  ┌────▼────┐
                  │ Grafana │
                  │(Visualize)│
                  └─────────┘
```

## 📋 Prerequisites

- **Python 3.8+**
- **Docker** and **Docker Compose**
- **Git**
- **2GB+ RAM** recommended for running monitoring stack

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/ArcTucruz/ecommerce-observability.git
cd ecommerce-observability
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file in the root directory:
```env
# Database Configuration
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=ecommerce.db

# Flask Configuration
SECRET_KEY=change-this-to-something-secret-in-production
FLASK_ENV=development
PORT=5001

# Logging
LOG_LEVEL=INFO

# Enable metrics
DEBUG_METRICS=1
```

### 4. Initialize Database
```bash
# Create admin user
python create_admin.py

# Add sample products (optional)
python add_sample_data.py
```

### 5. Run Application
```bash
python run.py
```

**Access the application:**
- **Frontend:** http://localhost:5001
- **Admin Dashboard:** http://localhost:5001/admin (login required)
- **Metrics Endpoint:** http://localhost:5001/metrics

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

## 📊 Monitoring Stack Setup

### 1. Start Monitoring Services
```bash
cd monitoring
docker-compose up -d
```

**This starts:**
- **Prometheus** (port 9090) - Metrics collection
- **Loki** (port 3100) - Log aggregation
- **Promtail** (port 9080) - Log shipper
- **Tempo** (port 3200, 4317, 4318) - Trace storage
- **Grafana** (port 3000) - Visualization

### 2. Access Grafana

**URL:** http://localhost:3000

**Default Login:**
- Username: `admin`
- Password: `admin`

### 3. Configure Data Sources

#### Add Prometheus:
1. Go to **Connections → Data sources → Add new data source**
2. Select **Prometheus**
3. **URL:** `http://prometheus:9090`
4. Click **Save & test**

#### Add Loki:
1. Click **Add new data source**
2. Select **Loki**
3. **URL:** `http://loki:3100`
4. Click **Save & test**

#### Add Tempo:
1. Click **Add new data source**
2. Select **Tempo**
3. **URL:** `http://tempo:3200`
4. Click **Save & test**

### 4. Explore Data

#### View Metrics (Prometheus):
```promql
# Total HTTP requests
flask_http_request_total

# Request rate (per second)
rate(flask_http_request_total[1m])

# Requests by status code
sum by (status) (flask_http_request_total)

# Business metrics
ecommerce_orders_total
ecommerce_cart_additions_total
```

#### View Logs (Loki):
```logql
# All application logs
{job="ecommerce-app"}

# Filter by log level
{job="ecommerce-app", level="INFO"}

# Search for specific text
{job="ecommerce-app"} |= "login"
```

#### View Traces (Tempo):
- Click **Explore** → Select **Tempo**
- Click **Search** to see all traces
- Click on any trace to see detailed request flow

## 🎨 Sample Queries

### Prometheus Metrics
```promql
# Average request duration
rate(flask_http_request_duration_seconds_sum[1m]) / 
rate(flask_http_request_duration_seconds_count[1m])

# Error rate (4xx and 5xx)
sum(rate(flask_http_request_total{status=~"4..|5.."}[5m]))

# Successful login rate
rate(ecommerce_user_logins_total{status="success"}[5m])
```

### Loki Log Queries
```logql
# Admin activity
{job="ecommerce-app"} |= "Admin"

# Errors only
{job="ecommerce-app", level="ERROR"}

# Parse JSON and filter
{job="ecommerce-app"} | json | logger="werkzeug"
```

## 🐳 Docker Services

| Service    | Port(s)      | Purpose                          |
|------------|--------------|----------------------------------|
| Flask App  | 5001         | E-commerce application           |
| Grafana    | 3000         | Visualization & dashboards       |
| Prometheus | 9090         | Metrics storage & queries        |
| Loki       | 3100         | Log aggregation & storage        |
| Promtail   | 9080         | Log collection & forwarding      |
| Tempo      | 3200, 4317   | Trace storage & OTLP ingestion   |

## 📁 Project Structure
```
ecommerce-observability/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── metrics.py           # Prometheus metrics
│   ├── tracing.py           # OpenTelemetry tracing
│   ├── models/              # Database models
│   ├── routes/              # Application routes
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── static/                  # CSS, JS, images
├── monitoring/
│   ├── docker-compose.yml   # Monitoring stack
│   ├── prometheus/          # Prometheus config
│   ├── loki/                # Loki config
│   ├── promtail/            # Promtail config
│   └── tempo/               # Tempo config
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── create_admin.py          # Admin user creation
└── add_sample_data.py       # Sample data loader
```

## 🛠️ Management Commands

### Stop All Services
```bash
# Stop Flask app
# Press Ctrl+C in the terminal running Flask

# Stop monitoring stack
cd monitoring
docker-compose stop
```

### Restart Services
```bash
# Start monitoring stack
docker-compose start

# Check status
docker-compose ps

# View logs
docker-compose logs -f [service-name]
```

### Clean Up
```bash
# Remove containers and volumes
docker-compose down -v

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
```

## 🔍 Troubleshooting

### Application won't start
```bash
# Check if port 5001 is already in use
lsof -i :5001  # Mac/Linux
netstat -ano | findstr :5001  # Windows

# Recreate database
rm ecommerce.db
python create_admin.py
```

### Docker containers keep restarting
```bash
# Check logs
docker-compose logs [service-name]

# Check resource usage
docker stats

# Restart with fresh volumes
docker-compose down -v
docker-compose up -d
```

### Can't connect to Grafana data sources
- Make sure all containers are running: `docker-compose ps`
- Check if using correct URLs (service names, not localhost)
- Verify containers are on same network: `docker network inspect monitoring_default`

## 📚 Technologies Used

**Backend:**
- Flask - Web framework
- SQLAlchemy - ORM
- SQLite - Database

**Observability:**
- Prometheus - Metrics collection
- Loki - Log aggregation
- Tempo - Distributed tracing
- Grafana - Visualization
- OpenTelemetry - Instrumentation

**Monitoring Stack:**
- Docker - Containerization
- Docker Compose - Orchestration

## 📄 License

This project is for educational purposes.

## 👤 Author

**ArcTucruz**
- GitHub: [@ArcTucruz](https://github.com/ArcTucruz)

## 🙏 Acknowledgments

- Three Pillars of Observability: Metrics, Logs, and Traces
- OpenTelemetry for standardized instrumentation
- Grafana Labs for the amazing observability tools
