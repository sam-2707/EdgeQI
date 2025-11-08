#!/bin/bash

# EDGE-QI System Deployment Script
# Complete deployment for EDGE-QI platform

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
                # Handle positional arguments
                if [[ -z "$1" ]]; then
                    DEPLOY_MODE="$arg"
                elif [[ -z "$2" ]]; then
                    NUM_NODES="$arg"
                fi
                ;;
        esac
    done
}

show_help() {
    cat << EOF
EDGE-QI System Deployment Script

Usage: $0 [MODE] [NUM_NODES] [OPTIONS]

Arguments:
    MODE            Deployment mode: development|production|test (default: development)
    NUM_NODES       Number of edge nodes to deploy (default: 4)

Options:
    --training      Run ML model training pipeline
    --validate      Run system validation tests
    --help          Show this help message

Examples:
    $0 development 4
    $0 production 8 --training
    $0 test --validate

EOF
}

# Check system requirements
check_requirements() {
    log_section "Checking System Requirements"
    
    local missing_deps=()
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    else
        log_info "Python3 is available"
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        log_info "Installing pip..."
        sudo apt-get update -qq
        sudo apt-get install -y python3-pip
    else
        log_info "Pip is available"
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        missing_deps+=("nodejs")
    else
        log_info "Node.js is available"
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        missing_deps+=("npm")
    else
        log_info "npm is available"
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        missing_deps+=("docker.io")
    else
        log_info "Docker is available"
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        missing_deps+=("docker-compose")
    else
        log_info "Docker Compose is available"
    fi
    
    # Install missing dependencies
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_info "Installing missing dependencies: ${missing_deps[*]}"
        sudo apt-get update -qq
        sudo apt-get install -y "${missing_deps[@]}"
    fi
    
    log_info "System requirements check passed"
}

# Setup Python environment
setup_python_environment() {
    log_section "Setting Up Python Environment"
    
    # Create virtual environment if it doesn't exist
    if [[ ! -d "$PROJECT_ROOT/venv" ]]; then
        log_info "Creating Python virtual environment..."
        python3 -m venv "$PROJECT_ROOT/venv"
    fi
    
    # Activate virtual environment
    source "$PROJECT_ROOT/venv/bin/activate"
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip
    
    # Install core dependencies
    log_info "Installing Python dependencies..."
    pip install \
        fastapi \
        uvicorn \
        websockets \
        numpy \
        opencv-python \
        psycopg2-binary \
        redis \
        paho-mqtt \
        asyncio \
        aiofiles
    
    log_info "Python environment setup complete"
}

# Setup Node.js environment
setup_nodejs_environment() {
    log_section "Setting Up Node.js Environment"
    
    cd "$PROJECT_ROOT/frontend"
    
    # Install Node.js dependencies
    log_info "Installing Node.js dependencies..."
    npm install --legacy-peer-deps
    
    log_info "Node.js environment setup complete"
    cd "$PROJECT_ROOT"
}

# Start infrastructure services
start_infrastructure() {
    log_section "Starting Infrastructure Services"
    
    # Ensure Docker is running
    if ! systemctl is-active --quiet docker; then
        log_info "Starting Docker service..."
        sudo systemctl start docker
    fi
    
    # Add user to docker group if not already
    if ! groups | grep -q docker; then
        log_info "Adding user to docker group..."
        sudo usermod -aG docker $USER
        log_warn "Please log out and back in for docker group changes to take effect"
    fi
    
    # Stop any existing services
    log_info "Stopping existing services..."
    cd "$PROJECT_ROOT"
    docker-compose down -v || true
    
    # Start services
    log_info "Starting infrastructure services..."
    docker-compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 20
    
    log_info "Infrastructure services started"
}

# Build and start frontend
start_frontend() {
    log_section "Starting Frontend"
    
    cd "$PROJECT_ROOT/frontend"
    
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        log_info "Starting frontend in development mode..."
        npm run dev &
        FRONTEND_PID=$!
        echo $FRONTEND_PID > /tmp/edge-qi-frontend.pid
        log_info "Frontend started in background (PID: $FRONTEND_PID)"
    else
        log_info "Building frontend for production..."
        npm run build
        log_info "Frontend built successfully"
    fi
    
    cd "$PROJECT_ROOT"
}

# Start backend
start_backend() {
    log_section "Starting Backend"
    
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    
    cd backend
    
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        log_info "Starting backend in development mode..."
        uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
        BACKEND_PID=$!
        echo $BACKEND_PID > /tmp/edge-qi-backend.pid
        log_info "Backend started in background (PID: $BACKEND_PID)"
    fi
    
    cd "$PROJECT_ROOT"
}

# Deploy edge nodes
deploy_edge_nodes() {
    log_section "Deploying Edge Nodes"
    
    source "$PROJECT_ROOT/venv/bin/activate"
    
    # Create edge node configurations
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
    
    log_info "Edge node configurations created for $NUM_NODES nodes"
    
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        # Start first edge node as example
        log_info "Starting edge node 1 as example..."
        cd "$PROJECT_ROOT/edge_nodes"
        python edge_node_complete.py --config=configs/node_1.json &
        NODE_PID=$!
        echo $NODE_PID > /tmp/edge-qi-node-1.pid
        log_info "Edge node 1 started in background (PID: $NODE_PID)"
        cd "$PROJECT_ROOT"
    fi
}

# Check service health
check_service_health() {
    log_section "Checking Service Health"
    
    log_info "Checking infrastructure services..."
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        log_info "✓ Docker services are running"
    else
        log_error "✗ Docker services are not running properly"
    fi
    
    # Check if frontend is accessible (if running)
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        sleep 5  # Give services time to start
        if curl -s http://localhost:3000 > /dev/null; then
            log_info "✓ Frontend is accessible at http://localhost:3000"
        else
            log_warn "⚠ Frontend may still be starting..."
        fi
        
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            log_info "✓ Backend API is accessible at http://localhost:8000"
        else
            log_warn "⚠ Backend API may still be starting..."
        fi
    fi
}

# Print deployment summary
print_summary() {
    log_section "Deployment Summary"
    
    echo "🎉 EDGE-QI Platform Deployment Complete!"
    echo ""
    echo "Configuration:"
    echo "  Mode: $DEPLOY_MODE"
    echo "  Edge Nodes: $NUM_NODES"
    echo ""
    echo "Services:"
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        echo "  Frontend: http://localhost:3000 (Development)"
        echo "  Backend API: http://localhost:8000"
    fi
    echo "  MQTT Broker: localhost:1883"
    echo "  PostgreSQL: localhost:5432"
    echo "  Redis: localhost:6379"
    echo ""
    echo "Management Commands:"
    echo "  View Docker logs: docker-compose logs -f"
    echo "  Stop all services: docker-compose down"
    echo "  Stop background processes: pkill -f 'npm run dev' && pkill -f 'uvicorn'"
    echo ""
    
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        echo "Development Commands:"
        echo "  Start additional edge nodes: python edge_nodes/edge_node_complete.py --config=edge_nodes/configs/node_X.json"
        echo "  Monitor logs: tail -f /tmp/edge-qi-*.log"
        echo ""
    fi
    
    echo "🚀 Access the EDGE-QI dashboard at: http://localhost:3000"
    echo "📡 Monitor system performance and control traffic lights!"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up background processes..."
    
    # Kill background processes
    if [[ -f /tmp/edge-qi-frontend.pid ]]; then
        kill $(cat /tmp/edge-qi-frontend.pid) 2>/dev/null || true
        rm -f /tmp/edge-qi-frontend.pid
    fi
    
    if [[ -f /tmp/edge-qi-backend.pid ]]; then
        kill $(cat /tmp/edge-qi-backend.pid) 2>/dev/null || true
        rm -f /tmp/edge-qi-backend.pid
    fi
    
    if [[ -f /tmp/edge-qi-node-1.pid ]]; then
        kill $(cat /tmp/edge-qi-node-1.pid) 2>/dev/null || true
        rm -f /tmp/edge-qi-node-1.pid
    fi
    
    # Kill any remaining processes
    pkill -f "npm run dev" 2>/dev/null || true
    pkill -f "uvicorn" 2>/dev/null || true
    pkill -f "edge_node_complete.py" 2>/dev/null || true
}

# Set trap for cleanup
trap cleanup EXIT

# Main deployment function
main() {
    parse_args "$@"
    
    log_section "EDGE-QI Platform Deployment"
    echo "Mode: $DEPLOY_MODE | Nodes: $NUM_NODES"
    
    check_requirements
    setup_python_environment
    setup_nodejs_environment
    start_infrastructure
    start_frontend
    start_backend
    deploy_edge_nodes
    check_service_health
    print_summary
    
    if [[ "$DEPLOY_MODE" == "development" ]]; then
        log_info "Press Ctrl+C to stop all services"
        # Keep script running to maintain background processes
        while true; do
            sleep 10
        done
    fi
}

# Show help if requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Run main function with all arguments
main "$@"