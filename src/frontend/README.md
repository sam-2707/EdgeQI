# EDGE-QI Frontend

A professional, industry-standard React dashboard for the EDGE-QI Smart City Monitoring Platform.

## 🎨 Design System

### Theme
- **Color Scheme**: Black & White minimalist design
- **Typography**: Inter font family for modern, clean aesthetics
- **Components**: Custom-designed UI components with Tailwind CSS
- **Responsive**: Mobile-first, fully responsive layout

### Key Features
- ✅ Real-time WebSocket connections for live data
- ✅ Comprehensive dashboard with system metrics
- ✅ Edge node monitoring and management
- ✅ Live object detection visualization
- ✅ Advanced analytics with interactive charts
- ✅ Byzantine consensus protocol monitoring
- ✅ Real-time system logs with filtering
- ✅ Complete settings configuration
- ✅ Alert system with notifications
- ✅ Professional data tables and visualizations

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Navigate to frontend directory
cd EDGE_QI/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will open at `http://localhost:5173`

### Build for Production

```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Top navigation bar
│   │   ├── Sidebar.jsx         # Side navigation menu
│   │   └── pages/
│   │       ├── Dashboard.jsx   # Main dashboard
│   │       ├── EdgeNodes.jsx   # Node management
│   │       ├── Detection.jsx   # Object detection
│   │       ├── Analytics.jsx   # Analytics & reports
│   │       ├── Consensus.jsx   # Consensus monitoring
│   │       ├── Logs.jsx        # System logs
│   │       └── Settings.jsx    # Configuration
│   ├── contexts/
│   │   └── EdgeQIContext.jsx   # Global state management
│   ├── App.jsx                 # Main application component
│   ├── main.jsx               # Application entry point
│   └── index.css              # Global styles & Tailwind
├── index.html                  # HTML template
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── postcss.config.js          # PostCSS configuration
└── package.json               # Dependencies
```

## 🎯 Pages Overview

### 1. Dashboard
- Real-time system metrics
- Active node statistics
- Detection performance charts
- Energy consumption monitoring
- Recent detections table

### 2. Edge Nodes
- Grid view of all edge nodes
- Node status monitoring (Active/Idle/Fault)
- CPU, Memory, Network metrics
- Individual node details modal
- Filter by status

### 3. Detection
- Live video stream grid
- Real-time object detection results
- Detection confidence visualization
- Stream controls (play/pause/stop)
- Export detection data

### 4. Analytics
- Traffic volume trends
- Node performance metrics
- Detection distribution (pie chart)
- Bandwidth optimization comparison
- Energy efficiency analysis
- Exportable reports

### 5. Consensus
- Byzantine consensus monitoring
- Round-by-round consensus history
- Node voting visualization
- Fault tolerance metrics
- Success rate tracking
- Protocol configuration display

### 6. System Logs
- Real-time log streaming
- Filter by log level (Info/Warning/Error/Success)
- Search functionality
- Auto-scroll option
- Export logs to file
- Color-coded by severity

### 7. Settings
- System configuration
- Detection parameters
- Edge node settings
- Consensus algorithm options
- Energy optimization toggles
- Notification preferences

## 🔌 Backend Integration

The frontend connects to the backend via:

### REST API
- `GET /api/system/status` - System metrics
- `GET /api/nodes` - Edge node list
- `GET /api/detections` - Detection history
- `GET /api/analytics` - Analytics data

### WebSocket Events
- `system_metrics` - Real-time metrics updates
- `edge_node_update` - Node status changes
- `detection_result` - New detection results
- `consensus_update` - Consensus round updates
- `system_log` - System log entries
- `alert` - System alerts

## 🎨 Styling

### Tailwind CSS Classes

Custom utility classes defined in `index.css`:

```css
.card                  # Card container
.btn-primary          # Primary button
.btn-secondary        # Secondary button
.btn-ghost           # Ghost button
.input               # Text input
.badge-success       # Success badge
.badge-warning       # Warning badge
.badge-error         # Error badge
.badge-info          # Info badge
.metric-card         # Metric card
.stat-value          # Stat value text
.stat-label          # Stat label text
```

### Color Palette

- **Black**: `#000000` - Background
- **White**: `#FFFFFF` - Primary text & buttons
- **Neutral-950**: `#0a0a0a` - Cards
- **Neutral-900**: `#171717` - Secondary backgrounds
- **Neutral-800**: `#262626` - Borders
- **Neutral-700**: `#404040` - Interactive elements
- **Neutral-500**: `#737373` - Muted text
- **Neutral-400**: `#a3a3a3` - Secondary text

## 📊 Charts & Visualizations

Using **Recharts** library for data visualization:

- Line Charts - Performance trends
- Area Charts - Traffic volume, energy
- Bar Charts - Detection statistics, comparisons
- Pie Charts - Distribution analysis

## 🔔 State Management

**EdgeQIContext** provides global state:

```javascript
const {
  connected,          // WebSocket connection status
  socket,            // Socket.io instance
  systemMetrics,     // System performance metrics
  edgeNodes,         // Edge node list
  detections,        // Detection results
  consensusData,     // Consensus history
  logs,              // System logs
  alerts,            // Active alerts
  dismissAlert,      // Dismiss alert function
  clearLogs,         // Clear logs function
  fetchSystemStatus, // Fetch system status
  fetchEdgeNodes,    // Fetch node list
} = useEdgeQI();
```

## 🌐 Environment Variables

Configure in `.env`:

```bash
VITE_BACKEND_URL=http://localhost:8000
VITE_WS_URL=http://localhost:8000
VITE_APP_NAME=EDGE-QI
VITE_APP_VERSION=1.0.0
```

## 🔧 Development

### Code Style
- ESLint for code linting
- Consistent component structure
- Functional components with hooks
- PropTypes for type checking

### Performance
- Code splitting by route
- Lazy loading for heavy components
- Optimized re-renders with React.memo
- Efficient WebSocket handling

## 📱 Responsive Design

Breakpoints:
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px  
- **Desktop**: > 1024px
- **Large Desktop**: > 1920px

## 🚀 Deployment

### Production Build

```bash
npm run build
```

Output in `dist/` directory. Serve with any static hosting:

- **Nginx**: Serve `dist` folder
- **Vercel**: Deploy with zero config
- **Netlify**: Connect repository
- **Docker**: Use provided Dockerfile

### Docker Deployment

```bash
docker build -t edge-qi-frontend .
docker run -p 80:80 edge-qi-frontend
```

## 📄 License

Part of the EDGE-QI project - Distributed Byzantine Fault Tolerant Quality-driven Intelligent Systems.

## 🤝 Contributing

Follow the project's contribution guidelines for code style, commits, and pull requests.

---

**Built with**: React 18, Vite 5, Tailwind CSS 3, Recharts 2, Socket.io Client 4
