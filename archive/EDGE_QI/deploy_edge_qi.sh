#!/bin/bash

"""
EDGE-QI System Deployment Script

This script sets up and deploys the complete EDGE-QI platform including:
- Infrastructure services (MQTT, PostgreSQL, Redis, Docker)
- ML training pipeline and model preparation
- Frontend and backend services
- Edge node deployment
- System validation and testing

From the paper:
"The EDGE-QI platform requires a comprehensive deployment strategy that
coordinates edge nodes, cloud infrastructure, and real-time communication
systems for optimal performance in smart traffic management scenarios."

Usage:
    ./deploy_edge_qi.sh [OPTIONS]
    
Options:
    --mode=production|development|test    Deployment mode (default: development)
    --nodes=N                            Number of edge nodes to deploy (default: 4)
    --training                           Run ML model training pipeline
    --validate                           Run system validation tests
    --help                              Show this help message

Example:
    ./deploy_edge_qi.sh --mode=development --nodes=4 --training --validate
"""

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
DEPLOY_MODE="${1:-development}"
NUM_NODES="${2:-4}"
RUN_TRAINING=false
RUN_VALIDATION=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}============================================${NC}\n"
}

# Parse command line arguments
parse_args() {
    for arg in "$@"; do
        case $arg in
            --mode=*)
                DEPLOY_MODE="${arg#*=}"
                ;;
            --nodes=*)
                NUM_NODES="${arg#*=}"
                ;;
            --training)
                RUN_TRAINING=true
                ;;
            --validate)
                RUN_VALIDATION=true
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $arg"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    cat << EOF
EDGE-QI System Deployment Script

Usage: $0 [OPTIONS]

Options:
    --mode=MODE          Deployment mode: production|development|test (default: development)
    --nodes=N           Number of edge nodes to deploy (default: 4)
    --training          Run ML model training pipeline
    --validate          Run system validation tests
    --help              Show this help message

Examples:
    $0 --mode=development --nodes=4
    $0 --mode=production --nodes=8 --training
    $0 --mode=test --validate

EOF
}

# Check system requirements
check_requirements() {
    log_section "Checking System Requirements"
    
    # Check if running on Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        log_error "This script is designed for Linux systems"
        exit 1
    fi
    
    # Check required commands
    local required_commands=("python3" "pip3" "node" "npm" "docker" "docker-compose" "git")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "$cmd is required but not installed"
            exit 1
        else
            log_info "$cmd is available"
        fi
    done
    
    # Check Python version (3.8+)
    local python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
        log_error "Python 3.8+ is required (found $python_version)"
        exit 1
    else
        log_info "Python $python_version is compatible"
    fi
    
    # Check Node.js version (16+)
    local node_version=$(node -v | sed 's/v//' | cut -d. -f1)
    if [[ $node_version -lt 16 ]]; then
        log_error "Node.js 16+ is required (found $node_version)"
        exit 1
    else
        log_info "Node.js $node_version is compatible"
    fi
    
    # Check available disk space (minimum 10GB)
    local available_space=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $4}')
    local space_gb=$((available_space / 1024 / 1024))
    if [[ $space_gb -lt 10 ]]; then
        log_warn "Low disk space: ${space_gb}GB available (10GB+ recommended)"
    else
        log_info "Sufficient disk space: ${space_gb}GB available"
    fi
    
    log_info "System requirements check passed"
}

# Install system dependencies
install_dependencies() {
    log_section "Installing System Dependencies"
    
    # Update package list
    log_info "Updating package lists..."
    sudo apt-get update -qq
    
    # Install system packages
    log_info "Installing system packages..."
    sudo apt-get install -y \
        build-essential \
        curl \
        wget \
        git \
        vim \
        htop \
        net-tools \
        mosquitto \
        mosquitto-clients \
        postgresql \
        postgresql-contrib \
        redis-server \
        nginx \
        python3-dev \
        python3-pip \
        python3-venv \
        libpq-dev \
        libssl-dev \
        libffi-dev \
        libjpeg-dev \
        libpng-dev \
        libopencv-dev \
        ffmpeg
    
    # Install Docker if not present
    if ! command -v docker &> /dev/null; then
        log_info "Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker "$USER"
        rm get-docker.sh
    fi
    
    # Install Docker Compose if not present
    if ! command -v docker-compose &> /dev/null; then
        log_info "Installing Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    log_info "System dependencies installed successfully"
}

# Setup Python environment
setup_python_environment() {
    log_section "Setting Up Python Environment"
    
    # Create virtual environment
    if [[ ! -d "$PROJECT_ROOT/venv" ]]; then
        log_info "Creating Python virtual environment..."
        python3 -m venv "$PROJECT_ROOT/venv"
    fi
    
    # Activate virtual environment
    source "$PROJECT_ROOT/venv/bin/activate"
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip setuptools wheel
    
    # Install Python dependencies
    log_info "Installing Python dependencies..."
    
    # Core dependencies
    pip install \
        fastapi \
        uvicorn \
        websockets \
        aiofiles \
        aiohttp \
        asyncio \
        numpy \
        pandas \
        scikit-learn \
        scipy \
        matplotlib \
        seaborn \
        opencv-python \
        Pillow \
        psycopg2-binary \
        redis \
        paho-mqtt \
        sqlalchemy \
        alembic \
        pydantic \
        python-multipart \
        python-jose \
        passlib \
        bcrypt \
        pytest \
        pytest-asyncio
    
    # ML/AI dependencies
    log_info "Installing ML/AI dependencies..."
    pip install \
        torch \
        torchvision \
        ultralytics \
        transformers \
        scikit-image \
        tensorflow \
        keras
    
    log_info "Python environment setup complete"
}

# Setup Node.js environment
setup_nodejs_environment() {
    log_section "Setting Up Node.js Environment"
    
    cd "$PROJECT_ROOT/frontend"
    
    # Install Node.js dependencies
    log_info "Installing Node.js dependencies..."
    npm install
    
    # Install additional development tools
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        npm install --save-dev \
            @types/node \
            @typescript-eslint/eslint-plugin \
            @typescript-eslint/parser \
            eslint \
            prettier \
            eslint-config-prettier \
            eslint-plugin-prettier
    fi
    
    log_info "Node.js environment setup complete"
}

# Setup infrastructure services
setup_infrastructure() {
    log_section "Setting Up Infrastructure Services"
    
    # Create Docker Compose file
    cat > "$PROJECT_ROOT/docker-compose.yml" << EOF
version: '3.8'

services:
  mosquitto:
    image: eclipse-mosquitto:2.0
    container_name: edge-qi-mosquitto
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - mosquitto_data:/mosquitto/data
      - mosquitto_logs:/mosquitto/log
      - ./infrastructure/mosquitto.conf:/mosquitto/config/mosquitto.conf
    restart: unless-stopped

  postgres:
    image: timescale/timescaledb:latest-pg14
    container_name: edge-qi-postgres
    environment:
      POSTGRES_DB: edge_qi
      POSTGRES_USER: edge_qi_user
      POSTGRES_PASSWORD: edge_qi_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infrastructure/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: edge-qi-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: edge-qi-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: edge-qi-backend
    environment:
      DATABASE_URL: postgresql://edge_qi_user:edge_qi_password@postgres:5432/edge_qi
      REDIS_URL: redis://redis:6379
      MQTT_BROKER: mosquitto
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - mosquitto
    volumes:
      - ./backend:/app
      - ./models:/app/models
    restart: unless-stopped

volumes:
  mosquitto_data:
  mosquitto_logs:
  postgres_data:
  redis_data:
EOF

    # Create infrastructure configuration files
    mkdir -p "$PROJECT_ROOT/infrastructure"
    
    # Mosquitto configuration
    cat > "$PROJECT_ROOT/infrastructure/mosquitto.conf" << EOF
listener 1883
allow_anonymous true
persistence true
persistence_location /mosquitto/data/

# WebSocket support
listener 9001
protocol websockets
allow_anonymous true

# Logging
log_dest file /mosquitto/log/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information
EOF

    # Database initialization script
    cat > "$PROJECT_ROOT/infrastructure/init-db.sql" << EOF
-- EDGE-QI Database Initialization

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS edge_nodes;
CREATE SCHEMA IF NOT EXISTS traffic_data;
CREATE SCHEMA IF NOT EXISTS consensus;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Edge nodes table
CREATE TABLE IF NOT EXISTS edge_nodes.nodes (
    node_id VARCHAR(50) PRIMARY KEY,
    intersection_id VARCHAR(50) NOT NULL,
    location JSONB,
    capabilities JSONB,
    status VARCHAR(20) DEFAULT 'offline',
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Traffic data table (hypertable for time-series)
CREATE TABLE IF NOT EXISTS traffic_data.measurements (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    node_id VARCHAR(50) NOT NULL,
    intersection_id VARCHAR(50) NOT NULL,
    vehicle_count INTEGER,
    queue_length REAL,
    avg_speed REAL,
    traffic_density REAL,
    anomaly_score REAL,
    metadata JSONB,
    FOREIGN KEY (node_id) REFERENCES edge_nodes.nodes(node_id)
);

-- Convert to hypertable
SELECT create_hypertable('traffic_data.measurements', 'time', if_not_exists => TRUE);

-- Consensus proposals table
CREATE TABLE IF NOT EXISTS consensus.proposals (
    proposal_id VARCHAR(50) PRIMARY KEY,
    proposer_id VARCHAR(50) NOT NULL,
    proposal_type VARCHAR(50) NOT NULL,
    target VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    parameters JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    executed_at TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (proposer_id) REFERENCES edge_nodes.nodes(node_id)
);

-- Consensus votes table
CREATE TABLE IF NOT EXISTS consensus.votes (
    vote_id VARCHAR(50) PRIMARY KEY,
    proposal_id VARCHAR(50) NOT NULL,
    voter_id VARCHAR(50) NOT NULL,
    vote_type VARCHAR(20) NOT NULL,
    confidence REAL,
    reasoning TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (proposal_id) REFERENCES consensus.proposals(proposal_id),
    FOREIGN KEY (voter_id) REFERENCES edge_nodes.nodes(node_id)
);

-- Analytics aggregations table
CREATE TABLE IF NOT EXISTS analytics.hourly_stats (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    intersection_id VARCHAR(50) NOT NULL,
    avg_vehicle_count REAL,
    avg_queue_length REAL,
    avg_speed REAL,
    total_anomalies INTEGER,
    energy_consumption REAL,
    bandwidth_usage REAL
);

-- Convert to hypertable
SELECT create_hypertable('analytics.hourly_stats', 'time', if_not_exists => TRUE);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_measurements_node_time ON traffic_data.measurements (node_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_measurements_intersection_time ON traffic_data.measurements (intersection_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON consensus.proposals (status);
CREATE INDEX IF NOT EXISTS idx_votes_proposal ON consensus.votes (proposal_id);

-- Create sample data
INSERT INTO edge_nodes.nodes (node_id, intersection_id, location, capabilities, status) VALUES
('node_1', 'intersection_1', '{"lat": 40.7128, "lon": -74.0060}', '{"cpu_cores": 4, "memory_gb": 8}', 'active'),
('node_2', 'intersection_2', '{"lat": 40.7589, "lon": -73.9851}', '{"cpu_cores": 4, "memory_gb": 8}', 'active'),
('node_3', 'intersection_3', '{"lat": 40.7505, "lon": -73.9934}', '{"cpu_cores": 4, "memory_gb": 8}', 'active'),
('node_4', 'intersection_4', '{"lat": 40.7282, "lon": -73.7949}', '{"cpu_cores": 4, "memory_gb": 8}', 'active')
ON CONFLICT (node_id) DO NOTHING;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA edge_nodes TO edge_qi_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA traffic_data TO edge_qi_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA consensus TO edge_qi_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO edge_qi_user;
EOF

    # Nginx configuration
    cat > "$PROJECT_ROOT/infrastructure/nginx.conf" << EOF
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            root /usr/share/nginx/html;
            try_files \$uri \$uri/ /index.html;
        }

        # API
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        # WebSocket
        location /ws {
            proxy_pass http://backend/ws;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
        }
    }
}
EOF

    log_info "Infrastructure configuration complete"
}

# Build and start services
start_services() {
    log_section "Starting Infrastructure Services"
    
    cd "$PROJECT_ROOT"
    
    # Stop any existing services
    log_info "Stopping existing services..."
    docker-compose down -v || true
    
    # Build and start services
    log_info "Building and starting services..."
    docker-compose up -d --build
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    check_service_health
    
    log_info "Infrastructure services started successfully"
}

# Check service health
check_service_health() {
    log_info "Checking service health..."
    
    # Check PostgreSQL
    if docker-compose exec -T postgres pg_isready -U edge_qi_user -d edge_qi; then
        log_info "✓ PostgreSQL is ready"
    else
        log_error "✗ PostgreSQL is not ready"
        return 1
    fi
    
    # Check Redis
    if docker-compose exec -T redis redis-cli ping | grep -q PONG; then
        log_info "✓ Redis is ready"
    else
        log_error "✗ Redis is not ready"
        return 1
    fi
    
    # Check Mosquitto
    if mosquitto_pub -h localhost -t test -m "health_check" -q 0; then
        log_info "✓ Mosquitto is ready"
    else
        log_error "✗ Mosquitto is not ready"
        return 1
    fi
}

# Run ML training pipeline
run_training_pipeline() {
    log_section "Running ML Training Pipeline"
    
    if [[ "$RUN_TRAINING" == true ]]; then
        cd "$PROJECT_ROOT"
        source venv/bin/activate
        
        log_info "Setting up training environment..."
        cd models
        chmod +x setup_training.sh
        ./setup_training.sh
        
        log_info "Downloading datasets..."
        python download_datasets.py
        
        log_info "Downloading pre-trained models..."
        python download_models.py
        
        log_info "Starting model training..."
        python train_yolo.py --dataset visdrone --epochs 10 --batch-size 16
        
        log_info "Quantizing models for edge deployment..."
        python quantize_models.py --input-model runs/detect/train/weights/best.pt
        
        log_info "ML training pipeline completed"
    else
        log_info "Skipping ML training pipeline (use --training to enable)"
    fi
}

# Deploy edge nodes
deploy_edge_nodes() {
    log_section "Deploying Edge Nodes"
    
    source "$PROJECT_ROOT/venv/bin/activate"
    
    # Create edge node configuration
    mkdir -p "$PROJECT_ROOT/edge_nodes/configs"
    
    for i in $(seq 1 $NUM_NODES); do
        cat > "$PROJECT_ROOT/edge_nodes/configs/node_${i}.json" << EOF
{
    "node_id": "node_${i}",
    "intersection_id": "intersection_${i}",
    "camera_id": $((i-1)),
    "yolo_model_path": "../models/yolov8n.pt",
    "known_nodes": [$(for j in $(seq 1 $NUM_NODES); do echo "\"node_${j}\""; done | paste -sd,)],
    "mqtt_broker": "localhost",
    "mqtt_port": 1883,
    "location": {
        "latitude": $((40 + i)),
        "longitude": $((74 + i))
    },
    "capabilities": {
        "max_compute_capacity": 2.5,
        "storage_capacity": 32.0,
        "camera_resolution": "1280x720",
        "ml_acceleration": true
    }
}
EOF
    done
    
    # Create systemd service files for edge nodes
    if [[ "$DEPLOY_MODE" == "production" ]]; then
        for i in $(seq 1 $NUM_NODES); do
            sudo tee "/etc/systemd/system/edge-qi-node-${i}.service" > /dev/null << EOF
[Unit]
Description=EDGE-QI Node ${i}
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_ROOT/edge_nodes
ExecStart=$PROJECT_ROOT/venv/bin/python edge_node_complete.py --config=configs/node_${i}.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        done
        
        # Enable and start services
        sudo systemctl daemon-reload
        for i in $(seq 1 $NUM_NODES); do
            sudo systemctl enable "edge-qi-node-${i}.service"
            sudo systemctl start "edge-qi-node-${i}.service"
        done
        
        log_info "Edge nodes deployed as systemd services"
    else
        log_info "Edge node configurations created for $NUM_NODES nodes"
        log_info "Use 'python edge_nodes/edge_node_complete.py --config=edge_nodes/configs/node_1.json' to start a node"
    fi
}

# Build and deploy frontend
deploy_frontend() {
    log_section "Deploying Frontend"
    
    cd "$PROJECT_ROOT/frontend"
    
    # Build frontend
    log_info "Building frontend..."
    npm run build
    
    if [[ "$DEPLOY_MODE" == "production" ]]; then
        # Copy build to nginx directory
        sudo cp -r dist/* /var/www/html/
        sudo systemctl restart nginx
        log_info "Frontend deployed to production"
    else
        log_info "Frontend built successfully"
        log_info "Access at http://localhost:3000 (development) or http://localhost (production)"
    fi
}

# Run system validation
run_validation() {
    log_section "Running System Validation"
    
    if [[ "$RUN_VALIDATION" == true ]]; then
        source "$PROJECT_ROOT/venv/bin/activate"
        
        log_info "Running algorithm tests..."
        cd "$PROJECT_ROOT/edge_nodes/algorithms"
        python -m pytest test_algorithm_1.py -v
        python -m pytest test_algorithm_2.py -v
        python -m pytest test_consensus.py -v
        
        log_info "Running integration tests..."
        cd "$PROJECT_ROOT"
        python -m pytest tests/ -v
        
        log_info "Testing API endpoints..."
        curl -f http://localhost:8000/health || log_error "Backend health check failed"
        curl -f http://localhost:8000/api/nodes || log_error "Nodes API failed"
        
        log_info "Testing MQTT connectivity..."
        mosquitto_pub -h localhost -t edge-qi/test -m "validation_test"
        
        log_info "System validation completed"
    else
        log_info "Skipping system validation (use --validate to enable)"
    fi
}

# Print deployment summary
print_summary() {
    log_section "Deployment Summary"
    
    echo "EDGE-QI Platform Deployment Complete!"
    echo ""
    echo "Configuration:"
    echo "  Mode: $DEPLOY_MODE"
    echo "  Edge Nodes: $NUM_NODES"
    echo "  Training: $RUN_TRAINING"
    echo "  Validation: $RUN_VALIDATION"
    echo ""
    echo "Services:"
    echo "  Frontend: http://localhost (Nginx)"
    echo "  Backend API: http://localhost:8000"
    echo "  MQTT Broker: localhost:1883"
    echo "  PostgreSQL: localhost:5432"
    echo "  Redis: localhost:6379"
    echo ""
    echo "Management Commands:"
    echo "  View logs: docker-compose logs -f"
    echo "  Stop services: docker-compose down"
    echo "  Restart services: docker-compose restart"
    echo ""
    
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        echo "Development Commands:"
        echo "  Start edge node: python edge_nodes/edge_node_complete.py --config=edge_nodes/configs/node_1.json"
        echo "  Start frontend dev: cd frontend && npm run dev"
        echo "  Start backend dev: cd backend && uvicorn main:app --reload"
        echo ""
    fi
    
    echo "Monitor the system at: http://localhost"
    echo ""
    echo "🎉 EDGE-QI Platform is ready for intelligent traffic management!"
}

# Main deployment function
main() {
    parse_args "$@"
    
    log_section "EDGE-QI Platform Deployment"
    echo "Mode: $DEPLOY_MODE | Nodes: $NUM_NODES | Training: $RUN_TRAINING | Validation: $RUN_VALIDATION"
    
    check_requirements
    install_dependencies
    setup_python_environment
    setup_nodejs_environment
    setup_infrastructure
    start_services
    
    if [[ "$RUN_TRAINING" == true ]]; then
        run_training_pipeline
    fi
    
    deploy_edge_nodes
    deploy_frontend
    
    if [[ "$RUN_VALIDATION" == true ]]; then
        run_validation
    fi
    
    print_summary
}

# Run main function with all arguments
main "$@"