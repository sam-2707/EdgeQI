# EDGE-QI Integration Plan

## Overview
Integrating the EDGE_QI subfolder (production frontend/backend) with the main folder (research simulations/papers) into one unified project structure.

## Current Structure Analysis

### Main Folder Contents:
- **Research/Academic**: IEEE paper, performance reports, LaTeX documents
- **Simulations**: Traffic simulation demos, realistic intersection simulations
- **Core Framework**: App/, Core/, ML/ directories with basic implementations
- **Analysis Tools**: Performance analysis scripts, data pipelines
- **Documentation**: Multiple README files, implementation status docs

### EDGE_QI Subfolder Contents:
- **Production Backend**: FastAPI server with complete API implementation
- **Production Frontend**: Next.js dashboard with real-time monitoring
- **ML Pipeline**: YOLOv8 training, quantization, VisDrone dataset integration
- **Edge Nodes**: Complete 8-layer architecture implementation
- **Infrastructure**: Docker setup, database configurations, deployment scripts

## Integration Strategy

### Phase 1: Directory Structure Consolidation
```
EDGE-QI/ (Main Root)
├── docs/                          # All documentation (merged)
│   ├── academic/                  # Research papers, reports
│   ├── api/                       # API documentation
│   ├── deployment/                # Deployment guides
│   └── user-guides/               # User manuals
│
├── src/                           # All source code
│   ├── backend/                   # FastAPI production backend
│   ├── frontend/                  # Next.js production frontend
│   ├── core/                      # Core EDGE-QI framework
│   ├── edge-nodes/               # Edge node implementations
│   ├── ml/                        # ML models and training
│   └── simulations/              # Traffic simulations
│
├── infrastructure/                # Deployment & infrastructure
│   ├── docker/                    # Docker configurations
│   ├── kubernetes/                # K8s configs (if needed)
│   └── scripts/                   # Deployment scripts
│
├── datasets/                      # ML training datasets
├── models/                        # Trained models
├── tests/                         # All test suites
├── tools/                         # Utility scripts and tools
│
├── README.md                      # Master README
├── QUICK_START.md                # Getting started guide
├── docker-compose.yml            # Main orchestration
└── requirements.txt              # Python dependencies
```

### Phase 2: Code Integration Tasks

#### 2.1 Backend Integration
- [x] Merge FastAPI backend from EDGE_QI/backend
- [x] Integrate with existing Core/ components
- [x] Consolidate database models
- [x] Merge API routers and services

#### 2.2 Frontend Integration
- [x] Use Next.js frontend as primary UI
- [x] Integrate with existing Streamlit dashboards (keep as alternative)
- [x] Consolidate monitoring components

#### 2.3 ML Pipeline Integration
- [x] Merge YOLOv8 training pipeline
- [x] Integrate model quantization
- [x] Consolidate ML models from both folders

#### 2.4 Edge Node Integration
- [x] Merge 8-layer edge node architecture
- [x] Integrate with existing Core/edge components
- [x] Consolidate consensus algorithms

#### 2.5 Infrastructure Integration
- [x] Merge Docker configurations
- [x] Consolidate deployment scripts
- [x] Integrate database setups

### Phase 3: Documentation Consolidation

#### 3.1 Create Master Documentation Structure
- Comprehensive README.md
- Quick Start Guide
- API Documentation
- Deployment Guide
- Academic/Research Papers Section

#### 3.2 Merge Existing Documentation
- IEEE Paper (academic/)
- Performance Reports (academic/)
- Implementation Guides (deployment/)
- API Documentation (api/)

### Phase 4: Configuration Consolidation

#### 4.1 Environment Configuration
- Single .env.example template
- Consolidated configuration files
- Unified deployment settings

#### 4.2 Dependency Management
- Merge requirements.txt files
- Consolidate package.json dependencies
- Remove duplicates

### Phase 5: Testing Integration

#### 5.1 Test Suite Consolidation
- Merge test files from both folders
- Create unified test structure
- Add integration tests

### Phase 6: Cleanup

#### 6.1 Remove Duplicates
- Identify and remove duplicate files
- Consolidate similar scripts
- Clean up temporary files

#### 6.2 Archive Old Structure
- Create backup of EDGE_QI subfolder
- Document migration

## Implementation Steps

### Step 1: Backup Current State
```bash
# Create backup of current structure
cp -r EDGE_QI EDGE_QI_backup_$(date +%Y%m%d)
```

### Step 2: Create New Directory Structure
```bash
# Create main directories
mkdir -p docs/{academic,api,deployment,user-guides}
mkdir -p src/{backend,frontend,core,edge-nodes,ml,simulations}
mkdir -p infrastructure/{docker,scripts}
mkdir -p tools
```

### Step 3: Move Files to New Structure

#### Academic/Research Content
```bash
mv *.tex *.pdf docs/academic/
mv *_REPORT.md *_ANALYSIS.md docs/academic/
mv NOVEL_CONTRIBUTIONS.md IMPLEMENTATION_STATUS.md docs/academic/
```

#### Source Code
```bash
# Backend
mv EDGE_QI/backend src/backend
# Frontend  
mv EDGE_QI/frontend src/frontend
# Core framework
mv Core src/core
mv App src/core/app
# ML
mv ML src/ml
mv EDGE_QI/models src/ml/training
# Edge nodes
mv EDGE_QI/edge_nodes src/edge-nodes
# Simulations
mv *_sim.py *_intersection.py src/simulations/
```

#### Infrastructure
```bash
mv EDGE_QI/docker infrastructure/docker
mv deploy*.sh infrastructure/scripts/
mv docker-compose.yml infrastructure/
```

#### Tools & Utilities
```bash
mv generate_*.py tools/
mv hardcoded_data_pipeline.py performance_analyzer.py tools/
mv verify_*.py check_*.py tools/
```

### Step 4: Consolidate Configuration

#### Merge Requirements
```bash
cat requirements.txt EDGE_QI/backend/requirements.txt | sort | uniq > requirements_merged.txt
mv requirements_merged.txt requirements.txt
```

#### Merge Environment Variables
```bash
cat .env.example EDGE_QI/backend/.env.example > .env.example.new
```

### Step 5: Update Imports and Paths

Update Python imports throughout the codebase:
```python
# Old: from Core.scheduler import *
# New: from src.core.scheduler import *

# Old: from edge_nodes.algorithms import *  
# New: from src.edge_nodes.algorithms import *
```

### Step 6: Create Master Documentation

Create comprehensive README.md covering:
- Project overview
- Both research and production aspects
- Quick start for different use cases
- Architecture documentation
- Links to detailed docs

### Step 7: Test Integration

```bash
# Test backend
cd src/backend && python main.py

# Test frontend
cd src/frontend && npm run dev

# Test simulations
python src/simulations/realistic_intersection_sim.py

# Run test suite
pytest tests/
```

### Step 8: Update Deployment Scripts

Update all deployment scripts to reflect new structure:
- docker-compose.yml paths
- deployment script paths
- CI/CD pipeline paths

## Timeline

- **Day 1**: Backup, create structure, move files (Steps 1-3)
- **Day 2**: Consolidate configs, update imports (Steps 4-5)
- **Day 3**: Documentation, testing (Steps 6-7)
- **Day 4**: Deployment updates, final validation (Step 8)

## Success Criteria

- ✅ All functionality from both folders working
- ✅ Single unified directory structure
- ✅ Comprehensive master documentation
- ✅ All tests passing
- ✅ Production deployment working
- ✅ Research simulations functional
- ✅ No duplicate files or code

## Rollback Plan

If integration issues occur:
1. Restore from EDGE_QI_backup
2. Review integration logs
3. Fix specific issues
4. Re-test before proceeding

## Notes

- Keep both Streamlit (simple) and Next.js (production) dashboards
- Maintain academic papers in separate docs/academic folder
- Preserve all training scripts and datasets
- Document any breaking changes in CHANGELOG.md
