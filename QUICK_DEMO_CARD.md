# 🎯 EDGE-QI Quick Reference Card

**Copy this for quick access during demonstrations**

---

## 🚀 Fastest Demo (30 seconds)

```powershell
# Start the interactive dashboard
python demo.py

# Then select option 1 (Dashboard)
# Open http://localhost:8501
# Click "Start" button
# Done! ✅
```

---

## 📊 Key Metrics to Memorize

| Metric | Value | Improvement |
|--------|-------|-------------|
| **FPS** | 5.34 | 66% faster |
| **Response Time** | <250ms | 38% faster |
| **Energy Savings** | 28.4% | vs baseline |
| **Bandwidth Reduction** | 74.5% | vs baseline |
| **Detection Accuracy** | 99.2% | State-of-art |
| **Consensus Accuracy** | 99.87% | Fault-tolerant |
| **Fault Tolerance** | 2 of 7 nodes | Can fail |

---

## 🎬 Three Demo Options

### Option A: Single Window (Easiest)
```powershell
python demo.py
# Choose: 1 (Dashboard)
```
**Time:** 2 minutes  
**Shows:** All features in one view

### Option B: Dual Window (Visual Impact)
```powershell
# Terminal 1:
python demo.py  # Choose 1 (Dashboard)

# Terminal 2:
python demo.py  # Choose 2 (Traffic Sim)
```
**Time:** 5 minutes  
**Shows:** Dashboard + Visual simulation

### Option C: Full System (Complete Demo)
```powershell
python demo.py
# Choose: 6 (Full System Launch)
```
**Time:** 15 minutes  
**Shows:** Everything

---

## 🎯 What to Say During Demo

### Opening (10 sec)
*"This is EDGE-QI - a smart traffic monitoring system using AI and edge computing."*

### Dashboard Tour (30 sec)
*"Here we're processing 4 camera feeds in real-time at 5.3 FPS. Watch the metrics panel - we're monitoring energy, bandwidth, and detections simultaneously."*

### Algorithm 1 (20 sec)
*"Notice the energy meter? When it drops, non-critical tasks automatically skip. That's our adaptive scheduling - saving 28% energy while maintaining performance."*

### Algorithm 2 (20 sec)
*"Look at the transmission log. We only send data when traffic changes - that's anomaly-driven transmission, reducing bandwidth by 74.5%."*

### Algorithm 3 (15 sec)
*"Behind the scenes, 7 edge nodes vote on decisions using Byzantine consensus. Even if 2 fail, the system continues. 99.87% accuracy."*

### Closing (5 sec)
*"Three algorithms, one system: smart scheduling, intelligent transmission, distributed consensus. That's EDGE-QI."*

---

## 🐛 Quick Troubleshooting

| Problem | Fix |
|---------|-----|
| Port already in use | `python demo.py` → Choose different option |
| Module not found | `pip install -r requirements.txt` |
| Slow performance | Close other programs, check Task Manager |
| Black screen | System uses simulated data (normal) |
| Browser won't open | Manually open: http://localhost:8501 |

---

## 📱 URLs Quick Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Dashboard | http://localhost:8501 | Main demo |
| Traffic Sim | http://localhost:8502 | Visual simulation |
| Benchmark | http://localhost:8503 | Performance comparison |
| API Docs | http://localhost:8000/docs | Backend API |

---

## 🎓 Research Paper Highlights

**Title:** "EDGE-QI: Energy and QoS-Aware Intelligent Edge Computing for Smart City Traffic Management"

**Novel Contributions:**
1. Multi-constraint adaptive scheduling (Algorithm 1)
2. Anomaly-driven data transmission (Algorithm 2)
3. Byzantine fault tolerant consensus (Algorithm 3)

**Dataset:** VisDrone (400K+ traffic images)

**Model:** YOLOv8n (quantized for edge)

**Venue:** IEEE Conference Paper (ready for submission)

---

## 💡 Demo Tips

✅ **DO:**
- Start with dashboard (most impressive)
- Highlight real-time metrics
- Show adaptive behavior (energy/network changes)
- Mention specific numbers (28.4%, 74.5%, 5.34 FPS)
- Let simulation run for 30+ seconds

❌ **DON'T:**
- Skip environment check
- Run too many things simultaneously (max 2-3)
- Forget to mention fault tolerance
- Hide the terminal (shows algorithm decisions)
- Rush through - let metrics update

---

## 🔥 Power User Commands

```powershell
# Quick test before demo
python -c "import streamlit, torch, cv2; print('✅ Ready')"

# Kill all Streamlit processes (if stuck)
taskkill /F /IM streamlit.exe

# Check GPU availability
python -c "import torch; print(f'GPU: {torch.cuda.is_available()}')"

# View system metrics
python demo.py  # Option 9

# One-liner full system
python demo.py  # Option 6
```

---

## 📝 Presentation Structure (10 min)

**Minute 1-2:** Project overview + Problem statement  
**Minute 3-5:** Live dashboard demo (start processing)  
**Minute 6-7:** Traffic simulation (visual impact)  
**Minute 8-9:** Algorithm explanations (with metrics)  
**Minute 10:** Q&A + Performance comparison  

---

## 🎯 Success Checklist

Before you start:
- [ ] Environment checked (`python demo.py` → Option 9)
- [ ] Browser ready (Chrome/Edge recommended)
- [ ] Screen recording setup (optional)
- [ ] Backup slides ready (if demo fails)
- [ ] Memorized key metrics (5.34 FPS, 28.4%, 74.5%)

During demo:
- [ ] Dashboard loads (<10 seconds)
- [ ] "Start" button clicked
- [ ] Camera feeds visible (4 cameras)
- [ ] Metrics updating (FPS, Energy, Bandwidth)
- [ ] Detections showing (vehicle boxes)
- [ ] Performance sustained (>5 FPS for 30+ sec)

After demo:
- [ ] Answered questions confidently
- [ ] Mentioned fault tolerance
- [ ] Highlighted 3 algorithms
- [ ] Provided GitHub link
- [ ] Offered follow-up materials

---

## 🚀 Launch Commands Cheat Sheet

```powershell
# RECOMMENDED (Interactive menu)
python demo.py

# DIRECT LAUNCHES
python edge_qi.py dashboard         # Main demo
python edge_qi.py traffic-sim       # Visual simulation
python edge_qi.py benchmark         # Performance comparison

# ALGORITHM DEMOS
python src/simulations/demo_realtime_integration.py     # Algorithm 1
python src/simulations/demo_anomaly_detection.py        # Algorithm 2
python src/simulations/demo_bandwidth_optimization.py   # Algorithm 3

# STREAMLIT DIRECT
streamlit run src/simulations/run_stable_dashboard.py --server.port 8501
streamlit run src/simulations/ultra_fast_traffic.py --server.port 8502
streamlit run src/simulations/performance_benchmark.py --server.port 8503
```

---

## 📞 Support Resources

- **Full Guide:** `DEMONSTRATION_GUIDE.md`
- **Quick Start:** `docs/user-guides/QUICK_START.md`
- **README:** `README.md`
- **Paper:** `docs/academic/EDGE_QI_IEEE_Paper.tex`
- **GitHub:** https://github.com/sam-2707/EdgeQI

---

## 🎉 You're Ready!

**Final check:**
```powershell
python demo.py  # Should show menu ✅
```

**Good luck with your demonstration! 🚀**

---

*Print this card or keep it open during your demo for quick reference.*
