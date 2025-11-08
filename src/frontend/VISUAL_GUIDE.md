# 🎨 EDGE-QI UI Visual Guide

## Color Palette

### Primary Colors
```
Black       #000000  ████████  Background
Neutral-950 #0a0a0a  ████████  Cards
Neutral-900 #171717  ████████  Secondary BG
Neutral-800 #262626  ████████  Borders
Neutral-700 #404040  ████████  Interactive
Neutral-600 #525252  ████████  
Neutral-500 #737373  ████████  Muted Text
Neutral-400 #a3a3a3  ████████  Secondary Text
White       #ffffff  ████████  Primary Text
```

### Accent Colors
```
Green-500   #22c55e  ████████  Success
Green-400   #4ade80  ████████  Success Light
Yellow-500  #eab308  ████████  Warning
Yellow-400  #facc15  ████████  Warning Light
Red-500     #ef4444  ████████  Error
Red-400     #f87171  ████████  Error Light
Blue-500    #3b82f6  ████████  Info
Blue-400    #60a5fa  ████████  Info Light
```

## Typography Scale

```
3xl:  text-3xl  30px  Bold      ← Main Metrics
2xl:  text-2xl  24px  Bold      ← Page Titles
xl:   text-xl   20px  Bold      ← Section Headers
lg:   text-lg   18px  Semibold  ← Card Titles
base: text-base 16px  Medium    ← Body Text
sm:   text-sm   14px  Regular   ← Labels
xs:   text-xs   12px  Regular   ← Meta Info
```

## Component Library

### Buttons

```
┌─────────────────┐
│   Primary       │  bg-white text-black hover:bg-neutral-200
└─────────────────┘

┌─────────────────┐
│   Secondary     │  bg-neutral-800 border border-neutral-700
└─────────────────┘

┌─────────────────┐
│   Ghost         │  hover:bg-white/10
└─────────────────┘
```

### Badges

```
┌──────────┐
│ Success  │  bg-green-500/10 text-green-400 border-green-500/20
└──────────┘

┌──────────┐
│ Warning  │  bg-yellow-500/10 text-yellow-400 border-yellow-500/20
└──────────┘

┌──────────┐
│  Error   │  bg-red-500/10 text-red-400 border-red-500/20
└──────────┘

┌──────────┐
│   Info   │  bg-blue-500/10 text-blue-400 border-blue-500/20
└──────────┘
```

### Cards

```
┌─────────────────────────────────────────┐
│  ┌────┐  Card Title                     │
│  │icon│                                  │
│  └────┘  Card content with               │
│          border-neutral-800              │
│          bg-neutral-950                  │
│          rounded-lg shadow-xl            │
│                                          │
└─────────────────────────────────────────┘
```

### Metric Cards

```
┌─────────────────────────────┐
│ ACTIVE NODES           ┌──┐ │
│                        │🔷│ │
│ 12/20                  └──┘ │
│ +2.5%                       │
└─────────────────────────────┘
```

### Tables

```
┌──────────────────────────────────────────────────────┐
│ Timestamp    Node ID    Type       Confidence  Action│
├──────────────────────────────────────────────────────┤
│ 08:42:15    node-01    Vehicle    ┌─────┐ 95% View  │
│ 08:42:14    node-02    Person     │█████│ 88% View  │
│ 08:42:13    node-01    Bicycle    └─────┘ 92% View  │
└──────────────────────────────────────────────────────┘
```

## Page Layouts

### Dashboard Layout
```
┌─────────────────────────────────────────────────────────┐
│ Header                                    🔔 Connected  │
├─────────────────────────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                       │
│ │ 12  │ │1,245│ │45ms │ │74%  │   ← Key Metrics       │
│ │Nodes│ │Detct│ │Ltncy│ │Band │                       │
│ └─────┘ └─────┘ └─────┘ └─────┘                       │
│                                                         │
│ ┌─────────────────────┐ ┌─────────────────────┐       │
│ │  Performance Chart  │ │  Energy Chart       │       │
│ │                     │ │                     │       │
│ │     ╱╲   ╱╲        │ │      ████            │       │
│ │    ╱  ╲ ╱  ╲       │ │      ████            │       │
│ │   ╱    ╲    ╲      │ │      ████            │       │
│ └─────────────────────┘ └─────────────────────┘       │
│                                                         │
│ ┌───────────────────────────────────────────┐         │
│ │  Recent Detections                        │         │
│ │  [Table with latest detection data]       │         │
│ └───────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### Edge Nodes Layout
```
┌─────────────────────────────────────────────────────────┐
│ Edge Nodes                      [All][Active][Idle][X]  │
├─────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│ │ ✓       │ │ ✓       │ │ ⚠       │ │ ✗       │       │
│ │ Node-01 │ │ Node-02 │ │ Node-03 │ │ Node-04 │       │
│ │ Active  │ │ Active  │ │ Idle    │ │ Fault   │       │
│ │         │ │         │ │         │ │         │       │
│ │ CPU 45% │ │ CPU 32% │ │ CPU  0% │ │ CPU N/A │       │
│ │ Mem 60% │ │ Mem 55% │ │ Mem 12% │ │ Mem N/A │       │
│ │ ⚡ 125W │ │ ⚡  98W │ │ ⚡  45W │ │ ⚡  N/A │       │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘       │
└─────────────────────────────────────────────────────────┘
```

### Detection Layout
```
┌─────────────────────────────────────────────────────────┐
│ Object Detection            [Grid][Single] [Filter ▾]   │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐                        │
│ │ 🔴 LIVE     │ │ 🔴 LIVE     │                        │
│ │             │ │             │                        │
│ │ Stream-01   │ │ Stream-02   │                        │
│ │ 30 FPS      │ │ 30 FPS      │                        │
│ └─────────────┘ └─────────────┘                        │
│                                                         │
│ ┌─────────────┐ ┌─────────────┐                        │
│ │ ⏸ IDLE      │ │ ⏸ IDLE      │                        │
│ │             │ │             │                        │
│ │ Stream-03   │ │ Stream-04   │                        │
│ │  0 FPS      │ │  0 FPS      │                        │
│ └─────────────┘ └─────────────┘                        │
│                                                         │
│ Detection Results                                       │
│ [Table with detection data]                             │
└─────────────────────────────────────────────────────────┘
```

## Icon System (Lucide React)

```
Navigation Icons:
📊 LayoutDashboard  - Dashboard
🌐 Network          - Edge Nodes
📷 Camera           - Detection
📈 BarChart3        - Analytics
🔀 GitBranch        - Consensus
📄 FileText         - Logs
⚙️  Settings         - Settings

Status Icons:
✓ CheckCircle       - Success/Active
⚠ AlertCircle       - Warning/Idle
✗ XCircle           - Error/Fault
ℹ Info              - Information
🔔 Bell             - Notifications

Metric Icons:
💻 Cpu              - CPU Usage
💾 HardDrive        - Memory/Storage
📡 Wifi             - Network
⚡ Zap              - Energy/Power
🖥️  Server           - Node/System
🏃 Activity         - Performance
🎯 Target           - Accuracy
⏱️  Clock            - Time/Latency
```

## Animations & Transitions

```css
/* Standard Transition */
transition-all duration-200

/* Hover Effects */
hover:bg-white/5
hover:border-neutral-700
hover:text-white

/* Loading States */
animate-pulse
animate-spin
animate-pulse-slow

/* Live Indicators */
bg-red-500 animate-pulse  /* Pulsing red dot */
```

## Spacing System

```
Gap Scale:
gap-1   4px    ▪▪
gap-2   8px    ▪ ▪
gap-3   12px   ▪  ▪
gap-4   16px   ▪   ▪
gap-6   24px   ▪     ▪

Padding Scale:
p-2     8px    Interior spacing
p-4     16px   Card padding
p-6     24px   Page padding

Margin Scale:
mb-2    8px    Small spacing
mb-4    16px   Medium spacing
mb-6    24px   Large spacing
```

## Responsive Grid

```
Mobile (< 640px):
grid-cols-1

Tablet (640px+):
grid-cols-2

Desktop (1024px+):
grid-cols-3 or grid-cols-4

Large (1920px+):
Full width with max-w-[1920px]
```

## Chart Styling

```javascript
// Recharts Configuration
<LineChart>
  <CartesianGrid 
    strokeDasharray="3 3" 
    stroke="#262626"    // neutral-800
  />
  <XAxis 
    stroke="#737373"    // neutral-500
    style={{ fontSize: '12px' }}
  />
  <YAxis 
    stroke="#737373"    // neutral-500
    style={{ fontSize: '12px' }}
  />
  <Tooltip
    contentStyle={{
      backgroundColor: '#0a0a0a',  // neutral-950
      border: '1px solid #262626', // neutral-800
      borderRadius: '8px',
    }}
  />
  <Line 
    stroke="#ffffff"    // white
    strokeWidth={2}
    dot={false}
  />
</LineChart>
```

## State Indicators

```
🟢 Active/Success    - Green pulsing dot
🟡 Warning/Idle      - Yellow static dot
🔴 Error/Fault       - Red pulsing dot
⚪ Offline/Unknown   - Gray static dot
```

## Best Practice Examples

### Card with Icon Header
```jsx
<div className="card p-6">
  <div className="flex items-center gap-3 mb-6">
    <div className="p-2 bg-white/5 rounded-lg">
      <Icon className="w-5 h-5" />
    </div>
    <h3 className="text-lg font-semibold">Card Title</h3>
  </div>
  {/* Content */}
</div>
```

### Metric Display
```jsx
<div className="metric-card">
  <p className="stat-label">LABEL</p>
  <span className="stat-value">Value</span>
  <p className="text-xs text-neutral-500 mt-1">Subtitle</p>
</div>
```

### Status Badge
```jsx
<span className="badge-success">Active</span>
<span className="badge-warning">Pending</span>
<span className="badge-error">Error</span>
<span className="badge-info">Info</span>
```

### Data Table Row
```jsx
<tr className="border-b border-neutral-800 hover:bg-white/5">
  <td className="py-3 px-4 text-sm">{data}</td>
</tr>
```

---

## 🎯 Design Principles

1. **Minimalism**: Less is more - clean, focused interface
2. **Consistency**: Uniform spacing, sizing, and behavior
3. **Hierarchy**: Clear visual importance through size and weight
4. **Contrast**: Black/white ensures maximum readability
5. **Feedback**: Hover states, transitions, loading indicators
6. **Accessibility**: High contrast, clear labels, keyboard nav
7. **Performance**: Optimized renders, lazy loading, code splitting
8. **Responsiveness**: Mobile-first, adaptive layouts

---

**Remember**: This is a professional monitoring dashboard - clarity and function over decoration!
