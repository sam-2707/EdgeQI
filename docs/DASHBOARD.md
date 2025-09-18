# EDGE-QI Real-time Dashboard

Advanced dashboard for real-time queue intelligence visualization, monitoring, and management. Provides comprehensive insights into queue detection, traffic analysis, multi-edge coordination, and system performance.

## Features

### 📊 Queue Analytics
- **Real-time Queue Heatmaps**: Interactive spatial visualization of queue densities and locations
- **Queue Type Distribution**: Pie charts showing distribution of vehicle, pedestrian, and mixed queues
- **Queue Statistics**: Live metrics including total queues, average wait times, maximum queue lengths, and density indicators
- **Confidence Tracking**: Visual indicators of detection confidence levels

### 🚗 Traffic Analytics
- **Multi-metric Time Series**: Real-time charts showing vehicle counts, average speeds, and congestion levels
- **Intersection Monitoring**: Live status of traffic intersections with signal phases and efficiency metrics
- **Flow Rate Analysis**: Comprehensive traffic flow analysis with historical trends
- **Congestion Detection**: Color-coded alerts and visual indicators for traffic congestion

### 🌐 Multi-Edge Network
- **Network Topology Visualization**: Interactive graph showing edge device positions and connections
- **Edge Status Monitoring**: Real-time status indicators (active, warning, error) for all edge devices
- **Load Balancing Visualization**: Visual representation of computational load distribution across edge nodes
- **Network Health Metrics**: Overall network health indicators and connectivity status

### ⚡ Performance Metrics
- **System Performance Gauges**: Real-time gauge charts for system load, memory usage, and processing rates
- **Detection Accuracy Tracking**: Live accuracy metrics for queue detection algorithms
- **Network Latency Monitoring**: Real-time network performance and communication latency
- **Consensus Success Rates**: Distributed consensus protocol performance metrics

### 🚨 Alerts & Notifications
- **Intelligent Alert System**: Automated detection and notification of system issues and traffic anomalies
- **Severity Classification**: Color-coded alerts with severity levels (critical, high, medium, low)
- **Alert Management**: Interactive alert dismissal and management capabilities
- **Location-based Alerts**: Spatial mapping of alerts to specific geographic coordinates

### 🎛️ Dashboard Controls
- **Data Simulation**: Start/stop simulation for demo and testing purposes
- **Auto-refresh**: Configurable auto-refresh intervals for real-time updates
- **Manual Refresh**: On-demand data refresh capabilities
- **System Status**: Live status indicators for all system components

## Architecture

### Dashboard Components

```
App/dashboard.py
├── DashboardState          # Central state management
├── Data Generation         # Simulation and real data handling
├── Visualization Charts    # Plotly-based interactive charts
├── Component Integration   # EDGE-QI framework integration
└── Web Interface          # Streamlit-based user interface
```

### Key Classes

#### `DashboardState`
Central state management for dashboard data including:
- Queue detection results
- Traffic flow metrics
- Edge network status
- Alert notifications
- Performance metrics
- Historical data storage

#### Visualization Functions
- `create_queue_heatmap()`: Interactive spatial queue visualization
- `create_traffic_flow_chart()`: Multi-metric traffic analysis charts
- `create_edge_network_topology()`: Network topology graph
- `create_performance_metrics_chart()`: System performance gauges

#### Data Management
- `generate_simulation_data()`: Realistic simulation data generation
- `init_dashboard_components()`: EDGE-QI framework integration
- `start_simulation()` / `stop_simulation()`: Simulation control

## Installation & Setup

### Dependencies
```bash
pip install streamlit>=1.25.0 plotly>=5.15.0 pandas>=2.0.0
```

### Quick Start
```bash
# Check dependencies
python run_dashboard.py --check-only

# Launch dashboard (default port 8501)
python run_dashboard.py

# Launch on custom port
python run_dashboard.py --port 8080

# Launch with debug logging
python run_dashboard.py --debug
```

### Direct Streamlit Launch
```bash
streamlit run App/dashboard.py --server.port 8501
```

## Usage Guide

### Starting the Dashboard
1. **Dependency Check**: Run `python run_dashboard.py --check-only` to verify all dependencies
2. **Launch**: Execute `python run_dashboard.py` to start the dashboard
3. **Access**: Open browser to `http://localhost:8501`

### Navigation
- **Sidebar Controls**: Use the left sidebar for simulation control and system status
- **Main Sections**: Navigate through Queue Analytics, Traffic Analytics, Multi-Edge Network, and Performance Metrics
- **Interactive Charts**: Click, zoom, and hover on charts for detailed information
- **Alerts Panel**: Monitor and manage system alerts in the notifications section

### Simulation Mode
- **Start Simulation**: Click "Start Simulation" in sidebar to begin data generation
- **Auto-refresh**: Enable auto-refresh for real-time updates every 2 seconds
- **Manual Control**: Use manual refresh button for on-demand updates
- **Stop Simulation**: Click "Stop Simulation" to pause data generation

## Integration

### EDGE-QI Framework Integration
The dashboard integrates with core EDGE-QI components:

```python
# Core component integration
from Core.queue.queue_detector import QueueDetector
from Core.traffic.traffic_analyzer import TrafficFlowAnalyzer
from Core.edge.edge_coordinator import EdgeCoordinator
from ML.tasks.surveillance_task import SurveillanceTask
```

### Real Data Sources
- **MQTT Integration**: Connect to MQTT brokers for real-time data feeds
- **Video Streams**: Integration with camera feeds and video processing pipelines
- **Edge Devices**: Direct connection to edge computing nodes for live metrics
- **Database Integration**: Historical data storage and retrieval capabilities

### API Endpoints
The dashboard can be extended with REST API endpoints for:
- Queue data retrieval
- Traffic metrics access
- Alert management
- System configuration

## Customization

### Adding New Visualizations
```python
def create_custom_chart():
    """Create custom visualization component"""
    fig = go.Figure()
    # Add custom chart logic
    return fig

# Integrate in main dashboard
st.plotly_chart(create_custom_chart(), use_container_width=True)
```

### Custom Data Sources
```python
def connect_custom_data_source():
    """Connect to custom data source"""
    # Implement custom data connection
    pass

# Add to dashboard initialization
def init_dashboard_components():
    connect_custom_data_source()
```

### Styling and Themes
- Modify Streamlit configuration in `.streamlit/config.toml`
- Customize Plotly chart themes and color schemes
- Add custom CSS for advanced styling

## Testing

### Test Suite
Comprehensive test coverage with 22 test cases:

```bash
# Run all dashboard tests
python -m pytest tests/test_dashboard.py -v

# Run specific test categories
python -m pytest tests/test_dashboard.py::TestVisualizationComponents -v
python -m pytest tests/test_dashboard.py::TestSimulationData -v
```

### Test Coverage
- **Dashboard State Management**: Initialization, data storage, component integration
- **Simulation Data Generation**: Queue data, traffic metrics, edge network status
- **Visualization Components**: Chart generation, data handling, edge cases
- **Component Integration**: EDGE-QI framework integration, error handling
- **Data Management**: Data limits, consistency, performance

### Performance Testing
- **Load Testing**: Simulate high-frequency data updates
- **Memory Testing**: Monitor memory usage with large datasets
- **Rendering Performance**: Test chart rendering with complex visualizations

## Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "App/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Environment Variables
```bash
EDGE_QI_DASHBOARD=1
STREAMLIT_SERVER_HEADLESS=true
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
```

### Security Considerations
- **Authentication**: Implement user authentication for production use
- **HTTPS**: Configure SSL/TLS for secure communication
- **Data Validation**: Validate all incoming data and user inputs
- **Access Control**: Implement role-based access control for sensitive operations

## Troubleshooting

### Common Issues

#### Import Errors
```bash
ImportError: cannot import name 'EdgeCoordinator'
```
**Solution**: Ensure all EDGE-QI framework components are properly installed and accessible.

#### Port Conflicts
```bash
Error: Port 8501 is already in use
```
**Solution**: Use a different port with `--port` flag or stop conflicting services.

#### Memory Issues
```bash
MemoryError: Unable to allocate array
```
**Solution**: Reduce simulation data size or increase system memory.

### Performance Optimization
- **Data Sampling**: Reduce data frequency for better performance
- **Chart Optimization**: Limit data points in time series charts
- **Memory Management**: Implement data cleanup for long-running sessions
- **Caching**: Use Streamlit caching for expensive computations

### Logging and Debugging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug mode
python run_dashboard.py --debug
```

## Future Enhancements

### Planned Features
- **Mobile Responsive Design**: Optimize for mobile and tablet viewing
- **Advanced Analytics**: Machine learning insights and predictive analytics
- **Export Capabilities**: PDF reports and data export functionality
- **Multi-language Support**: Internationalization and localization
- **Advanced Alerting**: Email notifications and webhook integrations

### API Development
- **REST API**: Comprehensive API for programmatic access
- **WebSocket Support**: Real-time bi-directional communication
- **GraphQL Integration**: Flexible data querying capabilities
- **Webhook Support**: Event-driven notifications and integrations

### Integration Expansions
- **Cloud Platforms**: AWS, Azure, GCP integration
- **IoT Platforms**: Direct IoT device integration
- **Smart City APIs**: Integration with municipal systems
- **Emergency Services**: Integration with emergency response systems