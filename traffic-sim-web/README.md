# 🚀 EDGE-QI 3D Traffic Simulation

High-performance real-time traffic intersection simulation built with **Next.js**, **Three.js**, and **WebGL**.

## ✨ Features

### 🎮 **3D WebGL Rendering**
- Real-time 3D intersection visualization
- Smooth 60 FPS performance
- Interactive camera controls
- Dynamic lighting and shadows

### 📹 **7 Strategic Cameras**
- North/South/East/West approach monitoring
- Center intersection coverage
- Northeast/Southwest corner cameras
- Real-time vehicle counting and tracking

### 🚦 **3 Traffic Signal System**
- Realistic signal timing cycles
- North-South main signal
- East-West cross signal
- Pedestrian crossing signal

### 📊 **Real-Time Analytics**
- Live vehicle count tracking
- Queue length monitoring
- Average speed calculations
- FPS performance metrics
- Interactive charts and graphs

### 🎨 **Modern UI/UX**
- Dark mode design
- Responsive layout
- Smooth animations with Framer Motion
- Tailwind CSS styling
- Real-time status indicators

## 🛠️ Technology Stack

- **Framework**: Next.js 14 (React 18)
- **3D Graphics**: Three.js + React Three Fiber
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Language**: TypeScript

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Navigate to the project directory
cd traffic-sim-web

# Install dependencies
npm install

# Run development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
# Build the project
npm run build

# Start production server
npm start
```

## 📁 Project Structure

```
traffic-sim-web/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx            # Root layout
│   └── page.tsx              # Main page
├── components/
│   ├── TrafficSimulation.tsx # 3D simulation component
│   ├── ControlPanel.tsx      # Simulation controls
│   ├── AnalyticsDashboard.tsx # Real-time analytics
│   ├── CameraView.tsx        # Camera status display
│   └── TrafficLight3D.tsx    # 3D traffic light model
├── store/
│   └── simulationStore.ts    # Zustand state management
├── lib/
│   ├── simulation.ts         # Simulation logic
│   └── utils.ts              # Utility functions
├── public/                   # Static assets
├── package.json              # Dependencies
├── tsconfig.json            # TypeScript config
├── tailwind.config.js       # Tailwind config
└── next.config.js           # Next.js config
```

## 🎮 How to Use

### Starting the Simulation
1. Click the **"Start Simulation"** button in the control panel
2. Watch vehicles appear and navigate the intersection
3. Observe real-time camera tracking and analytics

### Camera Controls
- **Rotate**: Left mouse button + drag
- **Zoom**: Mouse wheel
- **Pan**: Right mouse button + drag

### Control Panel Features
- ▶️ **Start/Stop**: Toggle simulation
- 🔄 **Reset**: Clear all vehicles and reset metrics
- ⚙️ **FPS Display**: Monitor performance
- 📊 **Live Metrics**: View real-time statistics

### Analytics Dashboard
- **Vehicle Count**: Total vehicles processed
- **Queue Lengths**: Traffic congestion monitoring
- **Average Speed**: Traffic flow analysis
- **Camera Status**: Individual camera metrics
- **Traffic Light States**: Signal timing visualization

## 🎨 Customization

### Adjust Simulation Speed
Edit `components/TrafficSimulation.tsx`:
```typescript
const SPAWN_RATE = 0.05 // Increase for more traffic
```

### Modify Camera Positions
Edit `store/simulationStore.ts`:
```typescript
const initialCameras: Camera[] = [
  { id: 'cam-north', position: [0, 5, 15], ... },
  // Adjust x, y, z coordinates
]
```

### Change Traffic Light Timing
Edit `store/simulationStore.ts`:
```typescript
cycleTime: { green: 30, yellow: 5, red: 35 } // Seconds
```

### Customize Colors
Edit `tailwind.config.js`:
```javascript
colors: {
  primary: '#3b82f6',    // Blue
  secondary: '#8b5cf6',   // Purple
  // Add your colors
}
```

## 🔧 Configuration

### Environment Variables
Create `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### Performance Optimization
- **Target FPS**: 60 (adjustable in simulation)
- **Vehicle Limit**: 50 concurrent (prevents lag)
- **Update Frequency**: 16ms (60 FPS)

## 📊 Performance Metrics

### Expected Performance
- **FPS**: 60 (desktop), 30+ (mobile)
- **Load Time**: < 2 seconds
- **Memory Usage**: < 100MB
- **CPU Usage**: Low (WebGL accelerated)

### Optimization Tips
1. Close unnecessary browser tabs
2. Use modern browser (Chrome/Firefox/Edge)
3. Enable hardware acceleration
4. Reduce vehicle spawn rate if needed

## 🐛 Troubleshooting

### Common Issues

**Simulation won't start:**
- Check browser console for errors
- Ensure WebGL is supported: `about:gpu` in Chrome
- Try clearing browser cache

**Low FPS:**
- Reduce vehicle spawn rate
- Close other applications
- Check GPU drivers are updated

**3D view not loading:**
- Ensure WebGL is enabled in browser
- Try different browser
- Check for console errors

**Build errors:**
- Delete `node_modules` and `.next` folders
- Run `npm install` again
- Check Node.js version (18+)

## 🚀 Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker
```bash
# Build image
docker build -t edge-qi-traffic-sim .

# Run container
docker run -p 3000:3000 edge-qi-traffic-sim
```

### Traditional Server
```bash
npm run build
npm start
# Configure reverse proxy (nginx/apache)
```

## 🔗 Integration with EDGE-QI Framework

### Launch from Main Framework
```bash
# From EDGE-QI root directory
python edge_qi.py web-sim
```

### API Endpoints
- `GET /api/simulation/status` - Get simulation state
- `POST /api/simulation/control` - Start/stop simulation
- `GET /api/analytics/metrics` - Fetch analytics data

## 📚 Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [Three.js Documentation](https://threejs.org/docs)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 🤝 Contributing

1. Follow TypeScript best practices
2. Use Tailwind for styling
3. Test on multiple browsers
4. Document new features
5. Optimize for performance

## 📄 License

Part of the EDGE-QI Framework project.

## 🎯 Roadmap

- [ ] Real camera feed integration
- [ ] ML-based traffic prediction
- [ ] Multi-intersection support
- [ ] Mobile app version
- [ ] VR/AR mode
- [ ] Advanced analytics
- [ ] Cloud deployment
- [ ] Real-time collaboration

---

**Built with ❤️ for the EDGE-QI Framework**

**Version**: 2.0  
**Last Updated**: October 16, 2025
