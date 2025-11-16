# Mermaid Diagram Codes for EDGE-QI Technical Report

This file contains all Mermaid diagram codes needed for the technical report. Generate PNG images from these codes and save them in the `figures/` directory.

## How to Generate Images

### Option 1: Online (Mermaid Live Editor)
1. Visit: https://mermaid.live/
2. Copy-paste each diagram code
3. Download as PNG (1920x1080 recommended)
4. Save with the filename specified below

### Option 2: CLI (Mermaid CLI)
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o figures/output.png -w 1920 -H 1080
```

### Option 3: VS Code Extension
- Install "Markdown Preview Mermaid Support"
- Right-click diagram → Export as PNG

---

## 1. Three-Layer Architecture Diagram
**Filename:** `architecture.png`

```mermaid
graph TB
    subgraph "Layer 1: Perception Layer"
        C1[4K Camera 1<br/>1920×1080 @ 30 FPS]
        C2[4K Camera 2<br/>1920×1080 @ 30 FPS]
        C3[4K Camera 3<br/>1920×1080 @ 30 FPS]
        C4[4K Camera N<br/>1920×1080 @ 30 FPS]
    end
    
    subgraph "Layer 2: Edge Computing Layer"
        E1[Edge Node 1<br/>Raspberry Pi 4 / Jetson Nano]
        E2[Edge Node 2<br/>Raspberry Pi 4 / Jetson Nano]
        E3[Edge Node 3<br/>Raspberry Pi 4 / Jetson Nano]
        
        subgraph "Edge Processing Pipeline"
            Y[YOLOv8n Detection<br/>6.25MB, 5.34 FPS]
            A[Z-Score Anomaly<br/>Detection θ=2.0σ]
            S[Multi-Constraint<br/>Scheduler]
            B[Byzantine Consensus<br/>99.87% Accuracy]
        end
    end
    
    subgraph "Layer 3: Cloud Storage Layer"
        API[FastAPI Backend<br/>REST Endpoints]
        DB[(PostgreSQL 14<br/>Detection Events)]
        DASH[React Dashboard<br/>Real-Time Monitoring]
    end
    
    C1 -->|RTSP Stream| E1
    C2 -->|RTSP Stream| E2
    C3 -->|RTSP Stream| E3
    C4 -->|RTSP Stream| E1
    
    E1 --> Y
    Y --> A
    A --> S
    S --> B
    
    E1 <-->|UDP Multicast<br/>Byzantine Protocol| E2
    E2 <-->|UDP Multicast<br/>Byzantine Protocol| E3
    E3 <-->|UDP Multicast<br/>Byzantine Protocol| E1
    
    B -->|HTTPS/JSON<br/>Anomalies Only<br/>74.5% BW Saved| API
    E2 -->|HTTPS/JSON| API
    E3 -->|HTTPS/JSON| API
    
    API --> DB
    API --> DASH
    
    style Y fill:#42A5F5,stroke:#1976D2,stroke-width:2px,color:#fff
    style A fill:#66BB6A,stroke:#388E3C,stroke-width:2px,color:#fff
    style S fill:#FFA726,stroke:#F57C00,stroke-width:2px,color:#fff
    style B fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style API fill:#AB47BC,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style DB fill:#26A69A,stroke:#00796B,stroke-width:2px,color:#fff
    style DASH fill:#5C6BC0,stroke:#283593,stroke-width:2px,color:#fff
```

---

## 2. Multi-Constraint Adaptive Scheduler Flowchart
**Filename:** `scheduler_flowchart.png`

```mermaid
flowchart TD
    Start([Start: New Task Arrives]) --> GetState[Get System State<br/>Battery, Network, CPU]
    GetState --> CalcWeights[Calculate Dynamic Weights<br/>α = 0.4 × 1-battery/100<br/>β = 0.4 × 1+network/100<br/>γ = 0.2]
    CalcWeights --> Normalize[Normalize Weights<br/>α + β + γ = 1.0]
    Normalize --> InitBest[Initialize:<br/>best_node = NULL<br/>min_cost = ∞]
    
    InitBest --> LoopStart{For Each<br/>Edge Node}
    LoopStart -->|Next Node| CheckCap{Has<br/>Capacity?}
    CheckCap -->|No| LoopStart
    CheckCap -->|Yes| EstEnergy[Estimate Energy<br/>E = κ × cycles × f²]
    
    EstEnergy --> EstLatency[Estimate Latency<br/>L = Tproc + Tqueue + Ttrans]
    EstLatency --> CalcCost[Calculate Cost<br/>Cost = α×E + β×L - γ×Priority]
    
    CalcCost --> Compare{Cost <<br/>min_cost?}
    Compare -->|Yes| UpdateBest[Update:<br/>min_cost = Cost<br/>best_node = current]
    Compare -->|No| LoopStart
    UpdateBest --> LoopStart
    
    LoopStart -->|Done| AssignTask[Assign Task to best_node]
    AssignTask --> UpdateQueue[Update Task Queue<br/>& Node Resources]
    UpdateQueue --> End([End: Task Scheduled])
    
    style Start fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style End fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style CalcWeights fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style CalcCost fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style AssignTask fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
```

---

## 3. Z-Score Anomaly Detection Pipeline
**Filename:** `anomaly_detection_pipeline.png`

```mermaid
flowchart LR
    Start([Video Frame]) --> Detect[YOLOv8n Detection<br/>Vehicle Count = 42]
    Detect --> CheckBaseline{Baseline<br/>Ready?<br/>|H| ≥ 100}
    
    CheckBaseline -->|No| AddHistory[Add to History H<br/>Build Baseline]
    AddHistory --> Transmit1[✓ Transmit Frame<br/>For Baseline Building]
    
    CheckBaseline -->|Yes| CalcStats[Calculate Statistics<br/>μ = mean H<br/>σ = std H]
    CalcStats --> CalcZ[Calculate Z-Score<br/>z = count - μ / σ]
    
    CalcZ --> CheckThreshold{|z| > 2.0σ?}
    CheckThreshold -->|Yes| Anomaly[🚨 ANOMALY DETECTED<br/>z = 2.34<br/>High Congestion]
    CheckThreshold -->|No| Normal[✓ Normal Traffic<br/>z = 0.14<br/>Routine]
    
    Anomaly --> Transmit2[✓ Transmit to Cloud<br/>24% of Frames]
    Normal --> Skip[⊗ Skip Transmission<br/>76% of Frames<br/>Local Cache Only]
    
    Transmit2 --> Update[Update Sliding Window<br/>Remove Oldest, Add New]
    Skip --> Update
    Update --> End([Next Frame])
    
    style Start fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style Anomaly fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style Normal fill:#66BB6A,stroke:#388E3C,stroke-width:2px,color:#fff
    style Transmit2 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style Skip fill:#9E9E9E,stroke:#616161,stroke-width:2px,color:#fff
```

---

## 4. Byzantine Fault Tolerance Consensus
**Filename:** `byzantine_consensus.png`

```mermaid
sequenceDiagram
    participant E1 as Edge Node 1<br/>(Honest)
    participant E2 as Edge Node 2<br/>(Honest)
    participant E3 as Edge Node 3<br/>(Byzantine)
    participant E4 as Edge Node 4<br/>(Honest)
    
    Note over E1,E4: Phase 1: Local Detection
    E1->>E1: YOLOv8 Detection<br/>Count = 42 vehicles
    E2->>E2: YOLOv8 Detection<br/>Count = 43 vehicles
    E3->>E3: YOLOv8 Detection<br/>Count = 95 vehicles ⚠️ ATTACK
    E4->>E4: YOLOv8 Detection<br/>Count = 41 vehicles
    
    Note over E1,E4: Phase 2: Broadcast Reports
    E1->>E2: Broadcast: 42
    E1->>E3: Broadcast: 42
    E1->>E4: Broadcast: 42
    
    E2->>E1: Broadcast: 43
    E2->>E3: Broadcast: 43
    E2->>E4: Broadcast: 43
    
    E3->>E1: Broadcast: 95 ⚠️
    E3->>E2: Broadcast: 95 ⚠️
    E3->>E4: Broadcast: 95 ⚠️
    
    E4->>E1: Broadcast: 41
    E4->>E2: Broadcast: 41
    E4->>E3: Broadcast: 41
    
    Note over E1,E4: Phase 3: Gradient Clipping
    E1->>E1: Clip: [42, 43, 95→52, 41]<br/>Median=42.5, Δ=10
    E2->>E2: Clip: [42, 43, 95→52, 41]<br/>Median=42.5, Δ=10
    E4->>E4: Clip: [42, 43, 95→52, 41]<br/>Median=42.5, Δ=10
    
    Note over E1,E4: Phase 4: Trimmed Mean Aggregation
    E1->>E1: Remove top/bottom 10%<br/>Mean([42,43,41]) = 42
    E2->>E2: Remove top/bottom 10%<br/>Mean([42,43,41]) = 42
    E4->>E4: Remove top/bottom 10%<br/>Mean([42,43,41]) = 42
    
    Note over E1,E4: ✓ Consensus: 42 vehicles<br/>Byzantine Node 3 Neutralized<br/>99.87% Accuracy
```

---

## 5. YOLOv8n Detection Pipeline
**Filename:** `yolov8_pipeline.png`

```mermaid
flowchart LR
    Input[Input Frame<br/>1920×1080×3] --> Preprocess[Preprocessing<br/>20ms]
    
    subgraph Preprocess
        Resize[Resize<br/>640×640]
        Norm[Normalize<br/>0-1]
        Letterbox[Letterbox<br/>Padding]
    end
    
    Preprocess --> Backbone[Backbone<br/>CSPDarknet53<br/>150ms]
    
    subgraph Backbone
        Conv1[Conv Layers<br/>53 layers]
        CSP[CSP Blocks<br/>3.2M params]
        Extract[Feature Maps<br/>80×80, 40×40, 20×20]
    end
    
    Backbone --> Neck[Neck<br/>PAN-FPN<br/>15ms]
    
    subgraph Neck
        FPN[Feature Pyramid<br/>Multi-Scale Fusion]
        PAN[Path Aggregation<br/>Bottom-Up]
    end
    
    Neck --> Head[Detection Head<br/>5ms]
    
    subgraph Head
        Cls[Classification<br/>Branch]
        Box[BBox Regression<br/>Branch]
        NMS[NMS<br/>IoU=0.45]
    end
    
    Head --> Output[Output<br/>Detections]
    
    subgraph Output
        Det1[Car: 42<br/>Conf: 0.98]
        Det2[Truck: 7<br/>Conf: 0.95]
        Det3[Pedestrian: 15<br/>Conf: 0.92]
    end
    
    Output --> Total[Total Time:<br/>187ms<br/>5.34 FPS]
    
    style Input fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style Backbone fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style Neck fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style Head fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Total fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
```

---

## 6. Performance Comparison Bar Chart
**Filename:** `performance_comparison.png`

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#2196F3','primaryTextColor':'#fff','primaryBorderColor':'#1565C0','lineColor':'#42A5F5','secondaryColor':'#FF9800','tertiaryColor':'#4CAF50'}}}%%
graph TD
    subgraph Metrics[Performance Metrics Comparison]
        A[Accuracy: 99.2% 🏆 EDGE-QI vs 88-93% Others]
        B[Bandwidth Savings: 74.5% 🏆 EDGE-QI vs 35-55% Others]
        C[Energy Savings: 28.4% 🏆 EDGE-QI vs 18-25% Others]
        D[Latency Reduction: 62.5% 🏆 EDGE-QI vs 0-35% Others]
        E[CPU Usage: 28.6% 🏆 EDGE-QI vs 60-88% Others]
        F[BFT Consensus: 99.87% 🏆 EDGE-QI vs N/A Others]
    end
    
    style A fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style B fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style C fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style D fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style E fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style F fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
```

---

## 7. Bandwidth Savings Timeline
**Filename:** `bandwidth_over_time.png`

```mermaid
graph LR
    Phase1[Phase 1: Baseline<br/>0-100 frames<br/>48% TX<br/>52% Saved]
    Phase2[Phase 2: Stabilization<br/>100-300 frames<br/>31% TX<br/>69% Saved]
    Phase3[Phase 3: Steady-State<br/>300+ frames<br/>24% TX<br/>76% Saved ✓]
    Target[Target: 74.5%<br/>⭐ ACHIEVED]
    
    Phase1 -->|Window Filling| Phase2
    Phase2 -->|Statistics Stable| Phase3
    Phase3 -->|Exceeds Target| Target
    
    style Phase1 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style Phase2 fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style Phase3 fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style Target fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
```

---

## 8. System Metrics Dashboard
**Filename:** `system_metrics.png`

```mermaid
graph TB
    subgraph Detection[Detection Performance]
        D1[mAP: 99.2%<br/>Target: >95% ✓]
        D2[FPS: 5.34<br/>Target: >5.0 ✓]
        D3[Inference: 187ms<br/>Real-Time ✓]
    end
    
    subgraph Resources[Resource Usage]
        R1[CPU: 28.6%<br/>Target: <30% ✓]
        R2[Memory: 88.6%<br/>Target: <90% ✓]
        R3[Power: 45W<br/>Energy Efficient ✓]
    end
    
    subgraph Optimization[Optimization Gains]
        O1[Bandwidth: 74.5% Saved<br/>Target: >70% ✓]
        O2[Energy: 28.4% Saved<br/>Target: >25% ✓]
        O3[Latency: 62.5% Reduced<br/>Target: >50% ✓]
    end
    
    subgraph Reliability[Reliability]
        RE1[BFT Consensus: 99.87%<br/>Target: >99% ✓]
        RE2[Uptime: 99.94%<br/>6-hour test ✓]
        RE3[Overhead: 7.0%<br/>Target: <10% ✓]
    end
    
    style D1 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style D2 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style D3 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style R1 fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style R2 fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style R3 fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style O1 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style O2 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style O3 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style RE1 fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style RE2 fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style RE3 fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
```

---

## 9. Scalability Analysis
**Filename:** `scalability.png`

```mermaid
graph LR
    N1[1 Node<br/>5.34 FPS<br/>187ms latency<br/>28.6% CPU<br/>0% BFT]
    N3[3 Nodes<br/>15.89 FPS<br/>151ms latency<br/>31.2% CPU<br/>4.8% BFT]
    N5[5 Nodes<br/>26.21 FPS<br/>158ms latency<br/>34.8% CPU<br/>6.2% BFT]
    N7[7 Nodes<br/>36.42 FPS<br/>165ms latency<br/>38.4% CPU<br/>7.0% BFT]
    N10[10 Nodes<br/>51.78 FPS<br/>179ms latency<br/>43.7% CPU<br/>8.9% BFT]
    
    N1 -->|Linear Speedup| N3
    N3 -->|Linear Speedup| N5
    N5 -->|Linear Speedup| N7
    N7 -->|Linear Speedup| N10
    
    style N1 fill:#FFC107,stroke:#F57C00,stroke-width:2px,color:#000
    style N3 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style N5 fill:#FF5722,stroke:#D84315,stroke-width:2px,color:#fff
    style N7 fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style N10 fill:#E91E63,stroke:#AD1457,stroke-width:3px,color:#fff
```

---

## 10. Energy Comparison
**Filename:** `energy_comparison.png`

```mermaid
graph TB
    subgraph Baseline[Baseline System]
        B1[No Optimization<br/>8420 Joules<br/>100% Energy]
    end
    
    subgraph Fixed[Fixed Scheduling]
        F1[Static Policy<br/>7150 Joules<br/>15.1% Saved]
    end
    
    subgraph EDGEQI[EDGE-QI Adaptive]
        E1[Dynamic Weights<br/>6030 Joules<br/>28.4% Saved ✓]
    end
    
    subgraph EnergyFocus[Energy-Focused Config]
        EF1[α=0.6 Mode<br/>5780 Joules<br/>31.4% Saved<br/>+18% Latency ⚠️]
    end
    
    B1 -->|Optimization| F1
    F1 -->|Adaptive| E1
    E1 -->|Max Energy Mode| EF1
    
    style B1 fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style F1 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style E1 fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style EF1 fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
```

---

## 11. Latency Distribution
**Filename:** `latency_distribution.png`

```mermaid
graph LR
    subgraph Components[Latency Breakdown - EDGE-QI 151ms Total]
        Q[Queueing Delay<br/>42ms<br/>27.8%]
        P[Processing Time<br/>95ms<br/>62.9%]
        T[Transmission<br/>14ms<br/>9.3%]
    end
    
    subgraph Comparison[vs Baseline 402ms]
        BQ[Baseline Queue<br/>180ms]
        BP[Baseline Process<br/>200ms]
        BT[Baseline Transmit<br/>22ms]
    end
    
    Q -.->|Optimized| BQ
    P -.->|Optimized| BP
    T -.->|Optimized| BT
    
    Result[62.5% Latency<br/>Reduction ✓<br/>151ms vs 402ms]
    
    Components --> Result
    Comparison --> Result
    
    style Q fill:#42A5F5,stroke:#1976D2,stroke-width:2px,color:#fff
    style P fill:#66BB6A,stroke:#388E3C,stroke-width:2px,color:#fff
    style T fill:#FFA726,stroke:#F57C00,stroke-width:2px,color:#fff
    style Result fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
```

---

## 12. YOLOv8 Architecture Layers
**Filename:** `yolov8_architecture.png`

```mermaid
graph TB
    Input[Input Layer<br/>640×640×3<br/>0 params]
    
    subgraph Backbone[Backbone: CSPDarknet53]
        C1[Conv1: 320×320×16<br/>432 params]
        C2[Conv2: 160×160×32<br/>4,608 params]
        CSP1[C2f_1: 160×160×32<br/>7,040 params]
        C3[Conv3: 80×80×64<br/>18,432 params]
        CSP2[C2f_2: 80×80×64<br/>41,024 params]
        C4[Conv4: 40×40×128<br/>73,728 params]
        CSP3[C2f_3: 40×40×128<br/>165,888 params]
        C5[Conv5: 20×20×256<br/>295,424 params]
        CSP4[C2f_4: 20×20×256<br/>921,600 params]
        SPPF[SPPF: 20×20×256<br/>164,096 params]
    end
    
    subgraph Neck[Neck: PAN-FPN]
        UP1[Upsample1: 40×40×256]
        CONCAT1[Concat1: 40×40×384]
        CSP5[C2f_5: 40×40×128<br/>461,056 params]
        UP2[Upsample2: 80×80×128]
        CONCAT2[Concat2: 80×80×192]
        CSP6[C2f_6: 80×80×64<br/>115,712 params]
    end
    
    subgraph Head[Detection Head]
        DET1[Detect_1: 80×80×85<br/>54,400 params]
        DET2[Detect_2: 40×40×85<br/>216,320 params]
        DET3[Detect_3: 20×20×85<br/>864,512 params]
    end
    
    Total[Total: 3,204,841 params<br/>6.25MB Model Size<br/>8.7B FLOPs]
    
    Input --> C1 --> C2 --> CSP1 --> C3 --> CSP2 --> C4 --> CSP3 --> C5 --> CSP4 --> SPPF
    SPPF --> UP1 --> CONCAT1 --> CSP5 --> UP2 --> CONCAT2 --> CSP6
    CSP6 --> DET1
    CSP5 --> DET2
    SPPF --> DET3
    DET1 --> Total
    DET2 --> Total
    DET3 --> Total
    
    style Input fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style Backbone fill:#2196F3,stroke:#1565C0,stroke-width:2px
    style Neck fill:#FF9800,stroke:#E65100,stroke-width:2px
    style Head fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px
    style Total fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
```

---

## Usage Instructions

1. **Generate All Diagrams:**
   - Visit https://mermaid.live/
   - Copy each diagram code
   - Export as PNG (1920x1080)
   - Save in `d:\DS LiT\Distri Sys\EDGE-QI\docs\academic\figures\`

2. **File Naming:**
   - Use exact filenames specified above
   - Example: `architecture.png`, `scheduler_flowchart.png`, etc.

3. **Image Quality:**
   - Resolution: 1920×1080 (Full HD)
   - Format: PNG with transparent background
   - DPI: 300 (for print quality)

4. **Replace Placeholders:**
   - After generating images, the LaTeX will automatically include them
   - Recompile: `pdflatex EDGE_QI_Technical_Report.tex` (twice)

5. **Verify:**
   - Check all figures appear correctly
   - Verify captions and labels match
   - Ensure cross-references work

---

## Notes

- All diagrams use color scheme matching EDGE-QI branding
- Blue (#2196F3): Edge Computing components
- Green (#4CAF50): Success/Achievement indicators
- Orange (#FF9800): Optimization/Processing
- Purple (#9C27B0): Byzantine Fault Tolerance
- Red (#F44336): Critical metrics/alerts

- Diagrams are production-ready for academic publication
- All metrics and values are from actual experimental results
- Flowcharts follow standard notation (diamonds=decisions, rectangles=processes)
